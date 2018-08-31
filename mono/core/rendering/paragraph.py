import pyphen   # type: ignore
import random

from enum import Enum
from typing import List, Union, Optional, Type

from ..domain import document as d
from ..formatting import Formatter, FormatTag


random.seed(1337)

Alignment = Enum("Alignment", ["left", "center", "right", "justify"])

pyphen_dictionary = pyphen.Pyphen(lang="en_US")
wrap = pyphen_dictionary.wrap

Line = List[Union[FormatTag, str]]

# FIXME: Bug: '*italic*.' -> '<i>italic<i> .'
# spaces are added between punctuation and tagged text


def flatten(elements: d.TextElements) -> Line:
    result: List[Union[FormatTag, str]] = []
    for element in elements:
        if isinstance(element, str):
            result.append(element)
        elif isinstance(element, d.Unprocessed):
            result.append("<UNPROCESSED: %s>" % element.kind)
        else:
            tag = FormatTag(element.__class__.__name__)
            result.append(tag)
            result.extend(flatten(element.children))  # type: ignore
            result.append(tag.close_tag)
    return result


def align(
    text_elements: List[Union[d.TextElement, str]],
    alignment: Alignment,
    width: int,
    formatter: Optional[Type[Formatter]] = None
) -> List[str]:

    elements = flatten(text_elements)
    lines: List[Line] = [[]]
    open_tags: List[str] = []

    def line_length(line: Line, with_spaces=False) -> int:
        only_words = [e for e in line if isinstance(e, str)]
        length_words = sum(len(word) for word in only_words)
        if with_spaces:
            return len(only_words) + length_words
        return length_words

    def room_left(line: Line) -> int:
        return width - line_length(line, with_spaces=True)

    def end_line(next_word=None):
        next_line = []
        # Close all unclosed tags, and re-open them on the next line
        for kind in reversed(open_tags):
            lines[-1].append(FormatTag(kind=kind).close_tag)
        for kind in open_tags:
            next_line.append(FormatTag(kind=kind))
        if next_word:
            next_line.append(next_word)
        lines.append(next_line)

    # --- Step 1 --------------------------------------------------------------
    # Break up elements in lines (with hyphenation)
    # and cross tags over the line when tags are still open.

    for element in elements:
        line = lines[-1]

        if isinstance(element, FormatTag):
            tag = element
            if tag.open:
                open_tags.append(tag.kind)
            else:
                last_index = next(
                    i for i, k in list(enumerate(open_tags))[::-1]
                    if k == tag.kind
                )
                open_tags.pop(last_index)
            line.append(tag)
            continue

        word: str = element

        available = room_left(line)

        if len(word) <= available:
            line.append(word)
        else:
            hyphenized = wrap(word, available)

            if hyphenized:
                left, right = hyphenized
                line.append(left)
                end_line(next_word=right)
            else:
                end_line(next_word=word)

    # --- Step 2 --------------------------------------------------------------
    # Depending on alignment, insert appropriate amount of spaces between words

    for line in lines:
        if alignment == Alignment.justify:
            pass
        else:
            # Alignment is either left or right:
            # there will be only one space between words

            # Insert a space after each word except the last
            # (Start from the right for easy insertion)

            last = True
            for i in range(len(line) - 1, -1, -1):
                if isinstance(line[i], str):
                    if last:
                        last = False
                        continue
                    line[i] += " "

    # --- Step 3 --------------------------------------------------------------
    # Add necessary padding
    for line in lines:
        padding = " " * (width - line_length(line))

        if alignment == Alignment.left:
            line.append(padding)

        elif alignment == Alignment.right:
            line.insert(0, padding)

        elif alignment == Alignment.center:
            middle = len(padding) // 2
            left_padding = padding[:middle]
            right_padding = padding[middle:]
            line.insert(0, left_padding)
            line.append(right_padding)

    # --- Step 4 --------------------------------------------------------------
    # Finalize each line with formatting

    def format(elem):
        if isinstance(elem, str):
            return elem
        else:
            return formatter.format_tag(elem)

    def strings(line):
        if formatter is not None:
            return [format(elem) for elem in line]
        else:
            return [elem for elem in line if isinstance(elem, str)]

    joined = ["".join(strings(line)) for line in lines]

    return joined
