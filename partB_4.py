from functools import reduce

# Higher-order function
def cumulative_operation(operation):
    return lambda sequence: reduce(operation, sequence)

# Factorial function using the cumulative_operation
factorial = cumulative_operation(lambda x, y: x * y)

# Exponentiation function using the cumulative_operation
# We create a sequence where the base repeats exponent times
exponentiation = lambda base, exp: cumulative_operation(lambda x, y: x * y)([base] * exp)

# Example usage:

# Factorial of 5 (5! = 5 * 4 * 3 * 2 * 1)
factorial_result = factorial(range(1, 6))
print(factorial_result)  # Output: 120

# Exponentiation: 2^3 = 2 * 2 * 2
exponentiation_result = exponentiation(2, 3)
print(exponentiation_result)  # Output: 8
