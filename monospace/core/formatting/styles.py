from ..symbols import characters


def character_map(string, alphabet):
    return "".join(map(lambda char: alphabet.get(char, char), string))


def number_map(number_string, alphabet):
    n = int(number_string)
    return alphabet[n]


def number_map2(number_string, alphabet):
    return "".join(map(lambda digit: alphabet[int(digit)], number_string))


def small_caps(string):
    return character_map(string.upper(), characters.small_caps)


def monospace(string):
    return character_map(string, characters.monospace)


def circled(string):
    try:
        number = int(string)
        return number_map(number, characters.circled_numbers)
    except ValueError:
        return character_map(string, characters.circled_characters)


def fraction(nominator, denominator=None):
    if denominator is None:
        nominator, _, denominator = nominator.partition("/")
    return characters.fractions.get(
        (nominator, denominator),
        (
            number_map2(nominator, characters.superscript)
            + characters.fraction_slash
            + number_map2(denominator, characters.subscript)
        )
    )
