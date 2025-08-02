#ifndef __FUNC_H__
#define __FUNC_H__

/* macros */
#define EQ(A, B) (1 - (!!((A) ^ (B))))
#define NE(A, B) (!!((A) ^ (B)))
#define GT(A, B) (EQ(cmp_u128_compliant((A), (B)), 1))
#define LT(A, B) (EQ(cmp_u128_compliant((A), (B)), -1))
#define GE(A, B) (GT(A,B) | EQ(A, B))
#define LE(A, B) (LT(A,B) | EQ(A, B))

#define MAX_LEN 1000001
#define BIG_NUM_LIMBS 52000
#define MAX_BIT 128
#define MAX_DIGITS (BIG_NUM_LIMBS * 39 + 1)

__uint128_t increment(__uint128_t i);
__uint128_t decrement(__uint128_t i);
__uint128_t cla_add(__uint128_t a, __uint128_t b);
__uint128_t cla_sub(__uint128_t a, __uint128_t b);
__uint128_t mult(__uint128_t a, __uint128_t b);
int cmp_u128_compliant(__uint128_t a, __uint128_t b);
void mult_u128_to_u256(__uint128_t a, __uint128_t b, __uint128_t* high, __uint128_t* low);
void add_bignum(__uint128_t result[], int* result_size, __uint128_t a[], int a_size, __uint128_t b[], int b_size);


#endif // __FUNC_H__