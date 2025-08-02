#include <stdio.h>
#include "func.h"

#define MAX_BIT 128

int cmp_u128_compliant(__uint128_t a, __uint128_t b) {
    __uint128_t i = MAX_BIT;
    loop:
    if (EQ(i, 0)) goto end;
    i = decrement(i);
    __uint128_t a_bit = (a >> i) & 1;
    __uint128_t b_bit = (b >> i) & 1;
    if (a_bit ^ b_bit) {
        if (a_bit) return 1;
        if (b_bit) return -1;
    }
    goto loop;

    end:
    return 0;
}

__uint128_t cla_add(__uint128_t a, __uint128_t b) {
    __uint128_t s = 0;
    __uint128_t c = 0;
    __uint128_t i = 0;
    /* P and G */
    __uint128_t P = a ^ b;
    __uint128_t G = a & b;

    bit_calc:
    __uint128_t a_bit = (a >> i) & 1;
    __uint128_t b_bit = (b >> i) & 1;
    __uint128_t s_bit = a_bit ^ b_bit ^ c;

    s |= (s_bit << i);
    c = ((G >> i) & 1) | (((P >> i) & 1) & c);

    i = increment(i);
    if (LT(i, MAX_BIT)) goto bit_calc;

    return s;
}

__uint128_t mult(__uint128_t a, __uint128_t b) {
    __uint128_t i = 0;
    __uint128_t result = 0;
    mult_calc:
    if ((b >> i) & 1) {
        result = cla_add(result, a << i);
    }
    i = increment(i);
    if (LT(i, MAX_BIT)) goto mult_calc;

    return result;
}

__uint128_t increment(__uint128_t i) {
    __uint128_t carry = 1;
    loop:
    __uint128_t temp = i;
    i^=carry;
    carry = temp & carry;
    carry<<=1;
    if(NE(carry, 0)) goto loop;
    return i;
}

__uint128_t decrement(__uint128_t i) {
    __uint128_t borrow = 1;
    loop:
    __uint128_t temp = i;
    i^=borrow;
    borrow = (~temp) & borrow;
    borrow<<=1;
    if(NE(borrow, 0)) goto loop;
    return i;
}

__uint128_t main() {
    __uint128_t a,b;
    printf("Enter two unsigned integers (up to 128 bits each): ");
    scanf("%llu %llu", &a, &b);
    __uint128_t result = mult(a, b);
    printf("Result: %llu\n", (unsigned long long)result);
    return 0;
}