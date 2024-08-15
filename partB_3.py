from functools import reduce

def cumulative_sum_of_squares(lists):
    return list(map(
        lambda sublist: reduce(
            lambda acc, x: acc + x**2,
            filter(
                lambda num: num % 2 == 0,
                sublist
            ),
            0
        ),
        lists
    ))

# Example usage:
lists_of_numbers = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
result = cumulative_sum_of_squares(lists_of_numbers)
print(result)  # Output: [20, 100, 244]
