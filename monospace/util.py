from copy import copy


# https://stackoverflow.com/a/6300649
def intersperse(sequence, value):
    result = [copy(value) for _ in range(2 * len(sequence) - 1)]
    result[::2] = sequence
    return result
