from functools import reduce

count_palindromes = lambda lst: list(map(lambda sublist: reduce(lambda acc, s: acc + 1, filter(lambda s: s == s[::-1], sublist), 0), lst))

# Example usage:
lists_of_strings = [["madam", "hello", "racecar"], ["abc", "def", "ghi"], ["level", "deed", "noon"]]
result = count_palindromes(lists_of_strings)
print(result)
