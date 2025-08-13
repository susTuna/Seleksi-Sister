#include <stdio.h>
#include "func.h"

static __uint128_t big_a[MAX_DIGITS];
static __uint128_t big_b[MAX_DIGITS];
static __uint128_t big_result[MAX_DIGITS * 2];
static __uint128_t len_a, len_b, len_result;

__uint128_t cla_add(__uint128_t a, __uint128_t b) {
    __uint128_t sum = a ^ b;
    __uint128_t carry = (a & b) << 1;
    
    carry_loop:
    if (EQ(carry, 0)) goto add_done;
    __uint128_t temp = sum;
    sum ^= carry;
    carry = (temp & carry) << 1;
    goto carry_loop;
    
    add_done:
    return sum;
}

__uint128_t cla_sub(__uint128_t a, __uint128_t b) {
    return cla_add(a, cla_add(~b, 1));
}

__uint128_t mult(__uint128_t a, __uint128_t b) {
    __uint128_t result = 0;
    __uint128_t i = 0;
    
    mult_loop:
    if (EQ(a, 0)) goto mult_done;
    if (a & 1) {
        result = cla_add(result, b);
    }
    a >>= 1;
    b <<= 1;
    goto mult_loop;
    
    mult_done:
    return result;
}

__uint128_t increment(__uint128_t n) {
    __uint128_t mask = 1;
    
    inc_loop:
    if (NE(n & mask, mask)) {
        return n ^ mask;
    }
    n ^= mask;
    mask <<= 1;
    goto inc_loop;
}

__uint128_t decrement(__uint128_t n) {
    __uint128_t mask = 1;
    
    dec_loop:
    if (n & mask) {
        return n ^ mask;
    }
    n ^= mask;
    mask <<= 1;
    goto dec_loop;
}

void reset_bigint(__uint128_t *digits, __uint128_t *length) {
    __uint128_t i = 0;
    clear_loop:
    if (EQ(i, MAX_DIGITS * 2)) goto clear_done;
    digits[i] = 0;
    i = increment(i);
    goto clear_loop;
    
    clear_done:
    *length = 1;
}

void scale_by_ten(__uint128_t *digits, __uint128_t *length) {
    __uint128_t carry = 0;
    __uint128_t i = 0;
    
    scale_loop:
    if (EQ(i, *length)) goto handle_carry;
    
    __uint128_t product = mult(digits[i], 10);
    product = cla_add(product, carry);
    
    digits[i] = product & DIGIT_MASK;
    carry = product >> BASE_SIZE;
    
    i = increment(i);
    goto scale_loop;
    
    handle_carry:
    if (NE(carry, 0)) {
        digits[*length] = carry;
        *length = increment(*length);
    }
}

void str_to_bigint(const char *str, __uint128_t *digits, __uint128_t *length) {
    reset_bigint(digits, length);
    
    __uint128_t i = 0;
    parse_loop:
    if (EQ(str[i], 0)) goto parse_done;
    
    if (str[i] >= '0' && str[i] <= '9') {
        scale_by_ten(digits, length);
        __uint128_t digit_val = str[i] - '0';
        digits[0] = cla_add(digits[0], digit_val);

        if (digits[0] >= ((__uint128_t)1 << BASE_SIZE)) {
            __uint128_t carry = digits[0] >> BASE_SIZE;
            digits[0] &= DIGIT_MASK;
            
            __uint128_t pos = 1;
            propagate_carry:
            if (EQ(carry, 0)) goto carry_done;
            if (GE(pos, *length)) {
                *length = increment(pos);
                digits[pos] = 0;
            }
            digits[pos] = cla_add(digits[pos], carry);
            if (digits[pos] >= ((__uint128_t)1 << BASE_SIZE)) {
                carry = digits[pos] >> BASE_SIZE;
                digits[pos] &= DIGIT_MASK;
                pos = increment(pos);
                goto propagate_carry;
            }
            carry_done:;
        }
    }
    
    i = increment(i);
    goto parse_loop;
    
    parse_done:;
}

void normalize_length(__uint128_t *digits, __uint128_t *length) {
    __uint128_t new_len = *length;
    
    trim_loop:
    if (EQ(new_len, 1)) goto trim_done;
    __uint128_t check_pos = cla_sub(new_len, 1);
    if (NE(digits[check_pos], 0)) goto trim_done;
    new_len = decrement(new_len);
    goto trim_loop;
    
    trim_done:
    *length = new_len;
}

void bigint_multiply() {
    reset_bigint(big_result, &len_result);
    
    __uint128_t i = 0;
    outer_mult:
    if (EQ(i, len_a)) goto mult_complete;
    
    __uint128_t j = 0;
    inner_mult:
    if (EQ(j, len_b)) goto inner_complete;
    
    __uint128_t product = mult(big_a[i], big_b[j]);
    __uint128_t pos = cla_add(i, j);

    __uint128_t carry = product;
    add_carry:
    if (EQ(carry, 0)) goto carry_complete;
    
    if (GE(pos, len_result)) {
        len_result = increment(pos);
        big_result[pos] = 0;
    }
    
    __uint128_t sum = cla_add(big_result[pos], carry);
    big_result[pos] = sum & DIGIT_MASK;
    carry = sum >> BASE_SIZE;
    pos = increment(pos);
    goto add_carry;
    
    carry_complete:
    j = increment(j);
    goto inner_mult;
    
    inner_complete:
    i = increment(i);
    goto outer_mult;
    
    mult_complete:
    normalize_length(big_result, &len_result);
}

int is_bigint_zero(__uint128_t *digits, __uint128_t length) {
    return EQ(length, 1) && EQ(digits[0], 0);
}

__uint128_t divide_by_ten(__uint128_t *digits, __uint128_t *length) {
    __uint128_t remainder = 0;
    __uint128_t i = *length;
    
    div_loop:
    if (EQ(i, 0)) goto div_complete;
    i = decrement(i);
    
    __uint128_t current = (remainder << BASE_SIZE) | digits[i];
    digits[i] = current / 10;
    remainder = current % 10;
    
    goto div_loop;
    
    div_complete:
    if (GT(*length, 1) && EQ(digits[cla_sub(*length, 1)], 0)) {
        *length = decrement(*length);
    }
    
    return remainder;
}

void print_bigint_decimal(__uint128_t *digits, __uint128_t length) {
    if (is_bigint_zero(digits, length)) {
        printf("0");
        return;
    }

    __uint128_t temp_digits[MAX_DIGITS * 2];
    __uint128_t temp_length = length;
    __uint128_t i = 0;
    
    copy_loop:
    if (EQ(i, length)) goto copy_done;
    temp_digits[i] = digits[i];
    i = increment(i);
    goto copy_loop;
    
    copy_done:

    char result_str[10000];
    __uint128_t str_len = 0;
    
    convert_loop:
    if (is_bigint_zero(temp_digits, temp_length)) goto convert_done;
    __uint128_t digit = divide_by_ten(temp_digits, &temp_length);
    result_str[str_len] = '0' + digit;
    str_len = increment(str_len);
    goto convert_loop;
    
    convert_done:

    print_loop:
    if (EQ(str_len, 0)) goto print_done;
    str_len = decrement(str_len);
    printf("%c", result_str[str_len]);
    goto print_loop;
    
    print_done:;
}

void read_input_string(const char *prompt, char *buffer, __uint128_t max_size) {
    printf("%s", prompt);
    
    __uint128_t i = 0;
    int ch;
    
    read_loop:
    ch = getchar();
    if (ch == '\n' || ch == EOF || GE(i, cla_sub(max_size, 1))) {
        goto read_done;
    }
    
    buffer[i] = (char)ch;
    i = increment(i);
    goto read_loop;
    
    read_done:
    buffer[i] = '\0';
}

int main() {
    char input_str_a[5000];
    char input_str_b[5000];
    
    printf("Bitwise Multiplication Calculator\n");
    printf("============================================\n\n");
    
    read_input_string("Enter first number: ", input_str_a, 5000);
    read_input_string("Enter second number: ", input_str_b, 5000);
    
    printf("\nProcessing multiplication...\n");

    str_to_bigint(input_str_a, big_a, &len_a);
    str_to_bigint(input_str_b, big_b, &len_b);

    bigint_multiply();

    printf("\nResult: ");
    print_bigint_decimal(big_result, len_result);
    printf("\n\n");
    
    return 0;
}