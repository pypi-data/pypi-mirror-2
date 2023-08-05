#include "_lcs.h"
#include <string.h>
#include <xmmintrin.h>
#include <stdint.h>
#include <stdlib.h>
#include <limits.h>


// Expands the 8 low weight 8 bit unsigned integer
// to 8 16bits signed integer

static inline vInt16 expand_8_to_16(vUInt8 data)
{
	vUInt8 mask_00= _mm_setzero_si128();

	return _mm_unpacklo_epi8(data,mask_00);
}


// Load an SSE register with the next 8 first symbols

static inline vInt16 load8Symboles(const char* seq)
{
	vUInt8 s;
	s = _mm_loadu_si128((vUInt8*)seq);
	return expand_8_to_16(s);
}


// Allocate a band allowing to align sequences of length : 'length'

static inline band_t* allocateBand(int length,band_t *band)
{
	int size;

	size = (length + 7) * sizeof(vInt16);

	if (band==NULL)
	{
		band = malloc(sizeof(band_t));
		if (!band)
			return NULL;

		if ((posix_memalign(&(band->band),16,size)) ||
			(!(band->band)))
		{
			free(band);
			return NULL;
		}

		band->size = length;
	}
	else if (length > band->size)
	{
		vInt16 *old = band->band;
		if ((posix_memalign(&(band->band),16,size)) ||
		    (!(band->band)))
		{
			band->band=old;
			return NULL;
		}
		band->size=length;
		free(old);
	}


	// SHRT_MIN

	return band;
}

int fastLCSScore(const char* seq1, const char* seq2,band_t **band)
{
	int lseq1,lseq2;		// length of the both sequences

	int itmp;				// tmp variables for swap
	const char* stmp;		//

	int nbands;				// Number of bands of width eight in the score matrix
	int lastband;			// width of the last band

	vInt16  *mainband;
	int16_t *scores;



		// Made seq1 the shortest sequences
	lseq1=strlen(seq1);
	lseq2=strlen(seq2);

	if (lseq1 > lseq2)
	{
		itmp=lseq1;
		lseq1=lseq2;
		lseq2=itmp;

		stmp=seq1;
		seq1=seq2;
		seq2=stmp;
	}

	nbands = lseq1 / 8;			// You have 8 short int in a SSE register
	lastband = lseq1 - (nbands * 8);


}
