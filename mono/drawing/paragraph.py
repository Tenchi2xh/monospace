from enum import Enum
import pyphen
import random
random.seed(1337)

from ..compiler import FormatTag

pyphen_dictionary = pyphen.Pyphen(lang="en_US")
wrap = pyphen_dictionary.wrap

# FIXME: Language in context object? (for hyphen dic)

Alignment = Enum("Alignment", ["left", "center", "right", "justify"])

def align(text, alignment=Alignment.justify,
          formatting=None, formatter=None, width=80, offset=0):
    words = text.split()[::-1]
    words[-1] = " " * offset + words[-1]

    lines = [[]]
    unclosed_tags = []

    def room_left(line):
        if line and isinstance(line[0], str):
            return width - (len(line) + sum(len(word) for word in line))
        return width - (len(line) + sum(length for _, length, _ in line))

    def format_word(word, cursor, crop=0, new_line=False):
        # Crop is for when we have a hyphen, it is an additional character
        # that shouldn't count for the cursor update
        length = len(word)
        if not formatting:
            return (word, length, cursor + length - crop)

        formatted = ""

        if new_line:
            start_tags = ""
            for tag in unclosed_tags:
                start_tags += formatter.convert(tag)
            formatted += start_tags

        # NOTE: We assume formatting is sorted!
        # Also, we add a space that we will not write, because some formatting might be lost
        for i, char in enumerate(word + " "):

            in_crop = i > length - crop - 1
            at_format_cursor = formatting and formatting[0].cursor == cursor + i
            if at_format_cursor:
                tag = formatting.pop(0)

                if tag.start:
                    unclosed_tags.append(tag)
                else:
                    index = next((i for i, t in enumerate(unclosed_tags) if t.start and t.type == tag.type), None)
                    if index is not None:
                        unclosed_tags.pop(index)

                formatted += formatter.convert(tag)

            if i != len(word):
                formatted += char

        return (formatted, length, cursor + length - crop)

    def end_line():
        last_block = lines[-1][-1]
        end_tags = ""
        for tag in unclosed_tags:
            end_tags += formatter.convert(tag.flip())
        lines[-1][-1] = (last_block[0] + end_tags, *last_block[1:])

    cursor = -offset
    while words:
        word = words.pop()

        line = lines[-1]
        available = room_left(line)

        if len(word) <= available:
            word_block = _, _, new_cursor = format_word(word, cursor)
            cursor = new_cursor
            line.append(word_block)
        else:
            # FIXME: Add a marker for unbreakable words
            hyphenized = wrap(word, available)

            if hyphenized:
                word_block_1 = _, _, new_cursor = format_word(hyphenized[0], cursor, crop=1)
                line.append(word_block_1)
                end_line()
                word_block_2 = _, _, new_cursor = format_word(hyphenized[1], new_cursor, new_line=True)
                cursor = new_cursor
                lines.append([word_block_2])
            else:
                end_line()
                word_block = _, _, new_cursor = format_word(word, cursor, new_line=True)
                cursor = new_cursor
                lines.append([word_block])
        cursor += 1

    result = ""
    for i, line in enumerate(lines):
        # In-between padding
        if alignment == Alignment.justify:
            if i < len(lines) - 1:
                spaces_to_add = room_left(line) + 1
                candidates = list(range(len(line) - 1))  # - 1 because we don't want to
                                                         # add a space after the last word

                # Maybe we need to add more spaces than we have candidates
                population = candidates
                while spaces_to_add > len(population):
                    population.extend(candidates)

                offsets = random.sample(candidates, spaces_to_add)
                for offset in offsets:
                    word_block = line[offset]
                    line[offset] = (word_block[0] + " ", word_block[1] + 1, word_block[2] + 1)

        spaced = " ".join(word for word, _, _ in line)
        space_left = width - sum(length for _, length, _ in line) - (len(line) - 1)

        # Left padding
        if alignment == Alignment.right:
            result += space_left * " "
        elif alignment == Alignment.center:
            result += int(space_left / 2) * " "
        result += spaced

        # Right padding
        if alignment == Alignment.left or alignment == Alignment.justify:
            result += space_left * " "
        elif alignment == Alignment.center:
            result += (space_left - int(space_left / 2)) * " "
        result += "\n"

    return result
