import subprocess
import sys
import os
import time

def generate_test_cases():
    test_cases = []

    power_of_2_32 = str(2**32)
    test_cases.append(("2^32 * 2^32", power_of_2_32, power_of_2_32))

    power_of_10_1000 = "1" + "0" * 1000
    test_cases.append(("10^1000 * 10^1000", power_of_10_1000, power_of_10_1000))

    power_of_10_1000000 = "1" + "0" * 1000000
    test_cases.append(("10^1000000 * 10^1000000", power_of_10_1000000, power_of_10_1000000))

    test_cases.append(("Small test: 999 * 999", "999", "999"))
    test_cases.append(("Medium test: 123456789 * 123456789", "123456789", "123456789"))
    test_cases.append(("Large Fibonacci: F45 * F45", "1134903170", "1134903170"))
    
    return test_cases

def write_input_to_file(num1, num2, filename="input.txt"):
    with open(filename, 'w') as f:
        f.write(f"{num1}\n{num2}\n")

def run_calc_program(input_file="input.txt", output_file="output.txt"):
    try:
        compile_result = subprocess.run(
            ["gcc", "-o", "calc", "calc.c"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if compile_result.returncode != 0:
            print(f"Compilation failed: {compile_result.stderr}")
            return None

        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            start_time = time.time()
            
            result = subprocess.run(
                ["./calc"],
                stdin=infile,
                stdout=outfile,
                stderr=subprocess.PIPE,
                text=True,
                timeout=600
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
        if result.returncode == 0:
            with open(output_file, 'r') as f:
                output = f.read()
            return output, execution_time
        else:
            print(f"Program execution failed: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("Program execution timed out (>10 minutes)")
        return None
    except Exception as e:
        print(f"Error running program: {e}")
        return None

def verify_result(num1, num2, calc_result):
    try:
        expected = int(num1) * int(num2)
        lines = calc_result.split('\n')
        result_line = None
        for line in lines:
            if line.startswith("Result:"):
                result_line = line.replace("Result:", "").strip()
                break
        
        if result_line is None:
            return False, "Could not find result in output"
        
        try:
            actual = int(result_line)
            if actual == expected:
                return True, "Correct"
            else:
                return False, f"Mismatch detected"
        except ValueError:
            return False, f"Could not parse result: {result_line}"
            
    except Exception as e:
        return False, f"Verification error: {e}"

def calculate_expected_result_info(num1, num2):
    try:
        n1_len = len(num1)
        n2_len = len(num2)

        if num1.startswith("1") and all(c == "0" for c in num1[1:]) and num1 == num2:
            zeros = len(num1) - 1
            expected_len = 2 * zeros + 1
            return f"Expected result: 10^{2*zeros} (1 followed by {2*zeros} zeros, {expected_len} digits total)"

        if num1 == num2 == str(2**32):
            result = 2**64
            return f"Expected result: 2^64 = {result} ({len(str(result))} digits)"

        expected_digits = n1_len + n2_len
        return f"Expected result length: approximately {expected_digits-1} to {expected_digits} digits"
        
    except Exception as e:
        return f"Could not calculate expected result info: {e}"

def run_performance_test():
    print("=== Benchmark ===\n")
    
    test_cases = generate_test_cases()
    
    for i, (description, num1, num2) in enumerate(test_cases):
        print(f"Test {i+1}: {description}")
        print(f"Number 1 length: {len(num1)} digits")
        print(f"Number 2 length: {len(num2)} digits")
        print(calculate_expected_result_info(num1, num2))
        print("-" * 50)

        input_filename = f"test_input_{i+1}.txt"
        output_filename = f"test_output_{i+1}.txt"
        
        write_input_to_file(num1, num2, input_filename)

        print("Running calculation...")
        result = run_calc_program(input_filename, output_filename)
        
        if result is None:
            print("Test failed - program did not complete successfully\n")
            continue
            
        output, execution_time = result
        print(f"Execution time: {execution_time:.3f} seconds")

        if len(num1) < 20 and len(num2) < 20: 
            is_correct, message = verify_result(num1, num2, output)
            if is_correct:
                print(f"Result verification: {message}")
            else:
                print(f"Result verification: {message}")
        else:
            print("Skipping verification for very large numbers")

        lines = output.split('\n')
        for line in lines:
            if line.startswith("Result:"):
                result_str = line.replace("Result:", "").strip()
                if len(result_str) > 100:
                    print(f"Result preview: {result_str[:50]}...{result_str[-50:]}")
                    print(f"Result length: {len(result_str)} digits")

                    if num1 == num2 and num1.startswith("1") and all(c == "0" for c in num1[1:]):
                        zeros_in_input = len(num1) - 1
                        expected_zeros = 2 * zeros_in_input
                        if result_str.startswith("1") and all(c == "0" for c in result_str[1:]) and len(result_str) == expected_zeros + 1:
                            print(f"Powers of 10 verification: Correct (10^{expected_zeros})")
                        else:
                            print(f"Powers of 10 verification: Expected 1 followed by {expected_zeros} zeros")
                else:
                    print(f"Result: {result_str}")
                break
        
        print(f"Full output saved to: {output_filename}")
        print("\n" + "="*60 + "\n")

        try:
            os.remove(input_filename)
        except:
            pass

def interactive_test():

    print("=== Interactive Bitwise Multiplication ===\n")
    
    while True:
        try:
            print("Enter two numbers to multiply (or 'quit' to exit):")
            num1 = input("First number: ").strip()
            
            if num1.lower() == 'quit':
                break
                
            num2 = input("Second number: ").strip()
            
            if num2.lower() == 'quit':
                break

            try:
                int(num1)
                int(num2)
            except ValueError:
                print("Please enter valid integers only\n")
                continue

            write_input_to_file(num1, num2, "interactive_input.txt")
            result = run_calc_program("interactive_input.txt", "interactive_output.txt")
            
            if result is None:
                print("Calculation failed\n")
                continue
            
            output, execution_time = result
            print(f"\nCalculation completed in {execution_time:.3f} seconds")

            lines = output.split('\n')
            for line in lines:
                if line.startswith("Result:"):
                    result_str = line.replace("Result:", "").strip()
                    if len(result_str) > 100:
                        print(f"Result preview: {result_str[:50]}...{result_str[-50:]}")
                        print(f"Result length: {len(result_str)} digits")
                    else:
                        print(f"Result: {result_str}")
                    break

            if len(num1) < 20 and len(num2) < 20:
                is_correct, message = verify_result(num1, num2, output)
                print(f"Verification: {message}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}\n")

    for filename in ["interactive_input.txt", "interactive_output.txt"]:
        try:
            os.remove(filename)
        except:
            pass

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_test()
    else:
        run_performance_test()

if __name__ == "__main__":
    main()