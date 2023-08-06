#include "_lcs.h"

#include <string.h>
#include <stdlib.h>
#include <limits.h>

#include <stdio.h>




#define VSIZE (8)
#define VTYPE vInt16
#define STYPE int16_t
#define CMENB shrt
#define VMODE false
#define FASTLCSSCORE fastLCSScore16
#define INSERT_REG _MM_INSERT_EPI16
#define EXTRACT_REG _MM_EXTRACT_EPI16
#define EQUAL_REG  _MM_CMPEQ_EPI16
#define ADD_REG    _MM_ADD_EPI16
#define SET_CONST  _MM_SET1_EPI16
#define GET_MAX    _MM_MAX_EPI16
#define MIN_SCORE  INT16_MIN

#include "_lcs_fast.h"
