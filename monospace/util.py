

# https://stackoverflow.com/a/6300649
def intersperse(sequence, value):
    result = [value] * (2 * len(sequence) - 1)
    result[::2] = sequence
    return result
