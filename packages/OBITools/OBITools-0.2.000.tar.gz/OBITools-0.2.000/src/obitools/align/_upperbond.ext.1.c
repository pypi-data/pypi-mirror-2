#include <xmmintrin.h>
#include <string.h>
#include <stdio.h>
#include <inttypes.h>
#include <math.h>

#define ALIGN __attribute__((aligned(16)))
typedef __m128i vUInt8;
typedef __m128i vUInt16;
typedef __m128i vUInt64;


typedef union
    {
	    vUInt8 m;
	    uint8_t c[16];
    } uchar_v;

typedef union
	{
		vUInt16 m;
		uint16_t c[8];
	} ushort_v;

typedef union
	{
		vUInt64 m;
		uint64_t c[2];
	} uint64_v;

inline static vUInt8 loadm128(const char* data)
{
	vUInt8 tmp;
	memcpy(&tmp,data,16);
	return tmp;
}

inline static uchar_v hash4m128(uchar_v frag)
{
	uchar_v words;

	vUInt8 mask_03= _mm_set1_epi8(0x03);        // charge le registre avec 16x le meme octet
	vUInt8 mask_7F= _mm_set1_epi8(0x7F);
	vUInt8 mask_FC= _mm_set1_epi8(0xFC);

	frag.m = _mm_srli_epi64(frag.m,1);         // shift logic a droite sur 2 x 64 bits
	frag.m = _mm_and_si128(frag.m,mask_03);    // and sur les 128 bits


	words.m= _mm_slli_epi64(frag.m,2);
	words.m= _mm_and_si128(words.m,mask_FC);
	frag.m = _mm_srli_si128(frag.m,1);
	words.m= _mm_or_si128(words.m,frag.m);

	words.m= _mm_slli_epi64(words.m,2);
	words.m= _mm_and_si128(words.m,mask_FC);
	frag.m = _mm_srli_si128(frag.m,1);
	words.m= _mm_or_si128(words.m,frag.m);

	words.m= _mm_slli_epi64(words.m,2);
	words.m= _mm_and_si128(words.m,mask_FC);
	frag.m = _mm_srli_si128(frag.m,1);
	words.m= _mm_or_si128(words.m,frag.m);

	return words;
}

inline static int anyzerom128(vUInt8 data)
{
	vUInt8 mask_00= _mm_setzero_si128();
	uint64_v tmp;
	tmp.m = _mm_cmpeq_epi8(data,mask_00);
	return (int)(tmp.c[0]!=0 || tmp.c[1]!=0);
}

inline static void dumpm128(unsigned short *table,vUInt8 data)
{
	memcpy(table,&data,16);
}

int buildTable(const char* sequence, unsigned char *table, int *count)
{
	int overflow = 0;
	int wc=0;
	int i;
	vUInt8 mask_00= _mm_setzero_si128();

	uchar_v frag;
	uchar_v words;
	uchar_v zero;

	char* s;

	s=(char*)sequence;

	memset(table,0,256*sizeof(unsigned char));

	// encode ascii sequence with  A : 00 C : 01  T: 10   G : 11

	for(frag.m=_mm_loadu_si128((vUInt8*)s);
		! anyzerom128(frag.m);
		s+=12,frag.m=_mm_loadu_si128((vUInt8*)s))
	{
		words= hash4m128(frag);

		// printf("%d %d %d %d\n",words.c[0],words.c[1],words.c[2],words.c[3]);

		if (table[words.c[0]]<255)  table[words.c[0]]++;  else overflow++;
		if (table[words.c[1]]<255)  table[words.c[1]]++;  else overflow++;
		if (table[words.c[2]]<255)  table[words.c[2]]++;  else overflow++;
		if (table[words.c[3]]<255)  table[words.c[3]]++;  else overflow++;
		if (table[words.c[4]]<255)  table[words.c[4]]++;  else overflow++;
		if (table[words.c[5]]<255)  table[words.c[5]]++;  else overflow++;
		if (table[words.c[6]]<255)  table[words.c[6]]++;  else overflow++;
		if (table[words.c[7]]<255)  table[words.c[7]]++;  else overflow++;
		if (table[words.c[8]]<255)  table[words.c[8]]++;  else overflow++;
		if (table[words.c[9]]<255)  table[words.c[9]]++;  else overflow++;
		if (table[words.c[10]]<255) table[words.c[10]]++; else overflow++;
		if (table[words.c[11]]<255) table[words.c[11]]++; else overflow++;

		wc+=12;
	}

	zero.m=_mm_cmpeq_epi8(frag.m,mask_00);
	//printf("frag=%d %d %d %d\n",frag.c[0],frag.c[1],frag.c[2],frag.c[3]);
	//printf("zero=%d %d %d %d\n",zero.c[0],zero.c[1],zero.c[2],zero.c[3]);
	words = hash4m128(frag);

	if (zero.c[0]+zero.c[1]+zero.c[2]+zero.c[3]==0)
		for(i=0;zero.c[i+3]==0;i++,wc++)
			if (table[words.c[i]]<255) table[words.c[i]]++;  else overflow++;

	if (count) *count=wc;
	return overflow;
}

static inline vUInt16 partialminsum(vUInt8 ft1,vUInt8 ft2)
{
	vUInt8   mini;
	vUInt16  minilo;
	vUInt16  minihi;
	vUInt8 mask_00= _mm_setzero_si128();

	mini      = _mm_min_epu8(ft1,ft2);
	minilo    = _mm_unpacklo_epi8(mini,mask_00);
	minihi    = _mm_unpackhi_epi8(mini,mask_00);

	return _mm_adds_epu16(minilo,minihi);
}

int compareTable(unsigned char *t1, int over1, unsigned char* t2,  int over2)
{
	vUInt8   ft1;
	vUInt8   ft2;
	vUInt8  *table1=(vUInt8*)t1;
	vUInt8  *table2=(vUInt8*)t2;
	ushort_v summini;
	int      i;
	int      total;

	ft1 = _mm_loadu_si128(table1);
	ft2 = _mm_loadu_si128(table2);
	summini.m = partialminsum(ft1,ft2);
	table1++;
	table2++;


	for (i=1;i<16;i++,table1++,table2++)
	{
		ft1 = _mm_loadu_si128(table1);
		ft2 = _mm_loadu_si128(table2);
		summini.m = _mm_adds_epu16(summini.m,partialminsum(ft1,ft2));

	}

	// Finishing the sum process

	summini.m = _mm_adds_epu16(summini.m,_mm_srli_si128(summini.m,8)); // sum the 4 firsts with the 4 lasts
	summini.m = _mm_adds_epu16(summini.m,_mm_srli_si128(summini.m,4));

	total = summini.c[0]+summini.c[1];
	total+= (over1 < over2) ? over1:over2;

	return total;
}

int threshold4(int wordcount,double identity)
{
	int error;
	int lmax;

	wordcount+=3;
	error = (int)floor((double)wordcount * ((double)1.0-identity));
	lmax  = (wordcount - error) / (error + 1);
	// printf("length = %d  error= %d   lmax= %d\n",wordcount,error,lmax);
	if (lmax < 4)
		return 0;
	return    (lmax  - 3) \
			* (error + 1) \
			+ ((wordcount - error) % (error + 1));
}
