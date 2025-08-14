# Bitwise Multiplication Calculator

A specialized big integer multiplication calculator implemented in C using only bitwise operations, carry-lookahead adders, and goto statements for control flow. This project demonstrates low-level arithmetic operations without using standard arithmetic operators.

## Dependencies

### Required
- **GCC** - GNU Compiler Collection with `__uint128_t` support
- **Python 3** - For running the test suite

### Installation

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install gcc python3
```

#### Linux (Arch)
```bash
sudo pacman -S gcc python
```

## Building

The project uses a simple compilation command:

```bash
gcc -o calc src/calc.c
```

Or use the test script which handles compilation automatically:

```bash
cd src/
python3 test.py
```

## Usage

### Interactive Mode
Run the calculator directly:

```bash
./calc
```

The program will prompt you for two numbers:
```
Bitwise Multiplication Calculator
============================================

Enter first number: 123456789
Enter second number: 987654321

Processing multiplication...

Result: 121932631112635269
```

### Automated Testing
Run the comprehensive test suite:

```bash
cd src/
python3 test.py
```

For interactive testing:
```bash
python3 test.py --interactive
```

## Test Cases

The benchmark includes several challenging test cases:

1. **Small Numbers:** 999 × 999
2. **Medium Numbers:** 123456789 × 123456789  
3. **Large Powers:** 2³² × 2³²
4. **Massive Numbers:** 10¹⁰⁰⁰ × 10¹⁰⁰⁰
5. **Extreme Scale:** 10¹⁰⁰⁰⁰⁰⁰ × 10¹⁰⁰⁰⁰⁰⁰

## File Structure

```
no-8/
├── src/
│   ├── calc.c          # Main calculator implementation
│   ├── func.h          # Function declarations and macros
│   └── test.py         # Comprehensive test suite
└── README.md           # This file
```

## Testing and Verification

The Python test suite provides:
- **Automatic Verification:** Compares results with Python's built-in arithmetic
- **Performance Benchmarking:** Measures execution time for various input sizes
- **Edge Case Testing:** Tests powers of 2, powers of 10, and large Fibonacci numbers
- **Interactive Mode:** Manual testing with immediate feedback

Run specific test modes:
```bash
# Full benchmark suite
python3 test.py

# Interactive testing
python3 test.py --interactive
```

## Example Output

```
Test 1: Small test: 999 * 999
Number 1 length: 3 digits
Number 2 length: 3 digits
Expected result length: approximately 5 to 6 digits
--------------------------------------------------
Running calculation...
Execution time: 0.001 seconds
Result verification: Correct
Result: 998001
```