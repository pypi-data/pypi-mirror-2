#include <xmmintrin.h>
#include <stdint.h>

#define ALIGN __attribute__((aligned(16)))
typedef __m128i vUInt8;
typedef __m128i vInt16;

typedef struct {
	int16_t    size;
	vInt16    *band;
} band_t;

int fastLCSScore(const char* seq1, const char* seq2,band_t **band);
