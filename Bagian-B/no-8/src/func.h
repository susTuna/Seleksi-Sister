#ifndef __FUNC_H__
#define __FUNC_H__

#include <stdio.h>

/* macros */
#define EQ(A, B) (1 - (!!((A) ^ (B))))
#define NE(A, B) (!!((A) ^ (B)))
#define GT(A, B) (EQ(cmp_u128_compliant((A), (B)), 1))
#define LT(A, B) (EQ(cmp_u128_compliant((A), (B)), -1))
#define GE(A, B) (GT(A,B) | EQ(A, B))
#define LE(A, B) (LT(A,B) | EQ(A, B))

#define MODULUS 18446744069414584321ULL
#define PRIMITIVE_PRIME 7
#define MAX_LEN 131072
#define BIG_NUM_LIMBS 52000
#define MAX_BIT 128
#define BASE_SIZE 64
#define DIGIT_MASK (((__uint128_t)1 << BASE_SIZE) - 1)
#define MAX_DIGITS 2048

int cmp_u128_compliant(__uint128_t a, __uint128_t b);
__uint128_t increment(__uint128_t i);
__uint128_t decrement(__uint128_t i);
__uint128_t cla_add(__uint128_t a, __uint128_t b);
__uint128_t cla_sub(__uint128_t a, __uint128_t b);
__uint128_t mult(__uint128_t a, __uint128_t b);
void reset_bigint(__uint128_t *digits, __uint128_t *length);
void scale_by_ten(__uint128_t *digits, __uint128_t *length);
void str_to_bigint(const char *str, __uint128_t *digits, __uint128_t *length);
void normalize_length(__uint128_t *digits, __uint128_t *length);
void bigint_multiply();
int is_bigint_zero(__uint128_t *digits, __uint128_t length);
void print_bigint_decimal(__uint128_t *digits, __uint128_t length);
void read_input_string(const char *prompt, char *buffer, __uint128_t max_size);

#endif // __FUNC_H__