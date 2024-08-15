from functools import reduce

concat_with_space = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)

# Example usage:
strings = ["Hey","this", "is", "peleg", "project"]
result = concat_with_space(strings)
print(result)
