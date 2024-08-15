primes_desc = lambda lst: sorted([x for x in lst if x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))], reverse=True)

# Example usage:
numbers = [10, 3, 5, 7, 11, 4, 8]
print(primes_desc(numbers))  # Output: [11, 7, 5, 3]
