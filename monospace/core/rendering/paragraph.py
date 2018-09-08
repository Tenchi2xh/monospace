import pyphen   # type: ignore
import random

from copy import copy
from enum import Enum
from itertools import groupby
from dataclasses import dataclass
from typing import List, Union, Optional, Callable, Tuple

from ..domain import document as d
from ..formatting import FormatTag, Format


random.seed(1337)

Alignment = Enum("Alignment", ["left", "center", "right", "justify"])

Element = Union[FormatTag, str]

# TODO: Language in settings for hyphen dictionary
pyphen_dictionary = pyphen.Pyphen(lang="en_US")
wrap = pyphen_dictionary.wrap


def align(
    text_elements: List[Union[d.TextElement, str]],
    alignment: Alignment,
    width: int,
    format_func: Optional[Callable] = None,
    text_filter: Callable[[str], str] = lambda s: s
) -> List[str]:

    elements = flatten(text_elements)
    words = [Word(elems) for elems in split(elements, d.space)]

    Line = List[Union[Element, d.Space]]
    lines: List[Line] = [[]]
    open_tags: List[str] = []

    def line_length(line: Line, with_spaces=False) -> int:
        only_words = [e for e in line if isinstance(e, str)]
        length_words = sum(len(word) for word in only_words)
        if with_spaces:
            return length_words + line.count(d.space)
        return length_words

    def room_left(line: Line) -> int:
        return width - line_length(line, with_spaces=True)

    def append_word(word, line):
        for element in word.elems:
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
            else:
                line.append(element)
        line.append(d.space)

    def end_line(next_word=None):
        next_line = []
        # Remove trailing space first
        if lines[-1][-1] == d.space:
            lines[-1].pop()
        # Close all unclosed tags, and re-open them on the next line
        for kind in reversed(open_tags):
            lines[-1].append(FormatTag(kind=kind).close_tag)
        for kind in open_tags:
            # FIXME: Bug: original data object from tag is lost
            next_line.append(FormatTag(kind=kind))
        if next_word:
            append_word(next_word, next_line)
        lines.append(next_line)

    # --- Step 1 --------------------------------------------------------------
    # Break up elements in lines (with hyphenation)
    # and cross tags over the line when tags are still open.

    for word in words:
        line = lines[-1]

        available = room_left(line)

        if len(word) <= available:
            append_word(word, line)
        else:
            hyphenized = wrap(word.word(), available)

            if hyphenized:
                index = len(hyphenized[0]) - 1
                left, right = word.split_at(index)
                # Don't add a hyphen if the word is a compound word
                if not left.word().endswith("-"):
                    left += "-"
                append_word(left, line)
                end_line(next_word=right)
            else:
                end_line(next_word=word)

    end_line()
    lines.pop()

    # --- Step 2 --------------------------------------------------------------
    # Depending on alignment, insert appropriate amount of spaces between words

    for i, line in enumerate(lines):
        # For the last line, we will let it be left-aligned
        if alignment == Alignment.justify and i < len(lines) - 1:
            # To justify the paragraph, we will take a random sample
            # of words from the line and add a space to them

            # with_space=True because each word will get one space after
            spaces_to_add = width - line_length(line, with_spaces=True)
            indices_candidates = [
                i for i, elem in enumerate(line)
                if isinstance(elem, str)  # We can only add spaces to words
            ]
            indices_candidates.pop()  # No space after last word

            # If we have more spaces to add than candidates,
            # we need to double the population space.
            population: List[int] = copy(indices_candidates)
            while spaces_to_add > len(population):
                population.extend(indices_candidates)

            # print(line_length(line, with_spaces=True),
            #       len(population), spaces_to_add)
            # "Small_but_necessary_interruption:_This_online_book_isn’t_sup-"
            # print(line)

            indices = random.sample(population, spaces_to_add)
            for index in indices:
                assert isinstance(line[index], str)
                line[index] = line[index] + " "

        # Replace all Space object with single spaces:
        for i, e in enumerate(line):
            if isinstance(e, d.Space):
                line[i] = " "

    # --- Step 3 --------------------------------------------------------------
    # Add necessary padding
    for line in lines:
        padding = " " * (width - line_length(line, with_spaces=True))

        if alignment == Alignment.left or alignment == Alignment.justify:
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

    filtered_lines = [
        [text_filter(elem) if isinstance(elem, str) else elem for elem in line]
        for line in lines
    ]

    if format_func is not None:
        return [
            format_func(line)
            for line in filtered_lines
        ]
    else:
        return [
            "".join(elem for elem in line if isinstance(elem, str))
            for line in filtered_lines
        ]


@dataclass
class Word():
    elems: List[Element]

    def __len__(self):
        return len(self.word())

    def __iadd__(self, s: str):
        last_str_index = next(
            i for i, elem in list(enumerate(self.elems))[::-1]
            if isinstance(elem, str)
        )
        self.elems[last_str_index] += s
        return self

    def word(self) -> str:
        return "".join(elem for elem in self.elems if isinstance(elem, str))

    def split_at(self, index) -> Tuple["Word", "Word"]:
        left: List[Element] = []
        right: List[Element] = []
        i = 0
        for i, elem in enumerate(self.elems):
            if isinstance(elem, str):
                if i <= index < i + len(elem):
                    left.append(elem[:index - i])
                    right.append(elem[index - i:])
                    right.extend(self.elems[i + 1:])
                    break
            left.append(elem)
        return Word(left), Word(right)


def get_tag(element):
    if isinstance(element, d.CrossRef):
        return FormatTag(
            Format.CrossRef,
            data={"identifier": element.identifier}
        )
    return FormatTag(Format[element.__class__.__name__])


def flatten(elements: d.TextElements) -> List[Union[FormatTag, str]]:
    result: List[Union[FormatTag, str]] = []
    for element in elements:
        if isinstance(element, str):
            result.append(element)
        elif isinstance(element, d.Space):
            result.append(element)
        elif isinstance(element, d.Unprocessed):
            result.append("<%s>" % element.kind)
        else:
            tag = get_tag(element)
            result.append(tag)
            result.extend(flatten(element.children))  # type: ignore
            result.append(tag.close_tag)
    return result


def split(iterable, separator):
    groups = groupby(iterable, lambda e: e != separator)
    return (list(group) for b, group in groups if b)
