import pyphen   # type: ignore
import random

from copy import copy
from enum import Enum
from typing import List, Union, Optional, Callable

from ..domain import document as d
from ..formatting import FormatTag, Format


random.seed(1337)

Alignment = Enum("Alignment", ["left", "center", "right", "justify"])

# FIXME: Justify doesn't work, fix is as follows
# NOTE: This will also fix the issue where the dot in "*bold*." could wrap.
# Do a `split()` on `d.space`. Resulting groups are logical words
# Fix the code to work with that and that should be about it.
# Maybe make class Word with correct __len__ and have an add() which
# adds a string to the last str of the word

# TODO: Language in settings for hyphen dictionary
pyphen_dictionary = pyphen.Pyphen(lang="en_US")
wrap = pyphen_dictionary.wrap

Line = List[Union[FormatTag, str]]


def get_tag(element):
    if isinstance(element, d.CrossRef):
        return FormatTag(
            Format.CrossRef,
            data={"identifier": element.identifier}
        )
    return FormatTag(Format[element.__class__.__name__])


def flatten(elements: d.TextElements) -> Line:
    result: List[Union[FormatTag, str]] = []
    for element in elements:
        if isinstance(element, str):
            result.append(element)
        elif isinstance(element, d.Space):
            result.append(element)
        elif isinstance(element, d.Unprocessed):
            result.append("<UNPROCESSED: %s>" % element.kind)
        else:
            tag = get_tag(element)
            result.append(tag)
            result.extend(flatten(element.children))  # type: ignore
            result.append(tag.close_tag)
    return result


# FIXME: Bug: punctuation can be pushed to the next line on its own

def align(
    text_elements: List[Union[d.TextElement, str]],
    alignment: Alignment,
    width: int,
    format_func: Optional[Callable] = None,
    text_filter: Callable[[str], str] = lambda s: s
) -> List[str]:

    elements = flatten(text_elements)
    lines: List[Line] = [[]]
    open_tags: List[str] = []
    non_word_buffer: List[Union[d.Space, FormatTag]] = []

    def line_length(line: Line, with_spaces=False) -> int:
        only_words = [e for e in line if isinstance(e, str)]
        length_words = sum(len(word) for word in only_words)
        if with_spaces:
            return len(only_words) + length_words
        return length_words

    def room_left(line: Line) -> int:
        return width - line_length(line, with_spaces=True)

    def process_buffer(line):
        for element in non_word_buffer:
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
            elif isinstance(element, d.Space):
                line.append(element)
        non_word_buffer.clear()

    def end_line(next_word=None, also_process_buffer=False):
        next_line = []
        # Close all unclosed tags, and re-open them on the next line
        for kind in reversed(open_tags):
            lines[-1].append(FormatTag(kind=kind).close_tag)
        for kind in open_tags:
            # FIXME: Bug: original data object from tag is lost
            next_line.append(FormatTag(kind=kind))
        if next_word:
            if also_process_buffer:
                process_buffer(next_line)
            next_line.append(next_word)
        lines.append(next_line)

    # --- Step 1 --------------------------------------------------------------
    # Break up elements in lines (with hyphenation)
    # and cross tags over the line when tags are still open.

    for element in elements:
        line = lines[-1]

        if not isinstance(element, str):
            non_word_buffer.append(element)
            continue

        word: str = element

        available = room_left(line)

        if len(word) <= available:
            process_buffer(line)
            line.append(word)
        else:
            hyphenized = wrap(word, available)

            if hyphenized:
                left, right = hyphenized
                process_buffer(line)
                line.append(left)
                end_line(next_word=right)
            else:
                # We are breaking the line, we don't want to put
                # the trailing spaces at the beginning of the next line
                non_word_buffer = [
                    e for e in non_word_buffer
                    if not isinstance(e, d.Space)
                ]
                end_line(next_word=word, also_process_buffer=True)

    # No more word was on the line, but maybe some tags were there
    process_buffer(lines[-1])

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
        padding = " " * (width - line_length(line))

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

    filtered_lines: List[List[Union[FormatTag, str]]] = [
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
