from typing import List, Union
from dataclasses import dataclass, field


class TextElement:
    pass


class StructureElement:
    pass


Element = Union[StructureElement, TextElement, str]


# --- Structure Elements ------------------------------------------------------

@dataclass
class Text(StructureElement):
    elements: List[Union[TextElement, str]]
    notes: List["Text"] = field(default_factory=list)


@dataclass
class Chapter(StructureElement):
    title: Text


@dataclass
class SubChapter(StructureElement):
    title: Text
    subtitle: Text


@dataclass
class Section(StructureElement):
    title: Text


@dataclass
class Paragraph(StructureElement):
    text: Text


@dataclass
class Quote(StructureElement):
    text: Text


@dataclass
class OrderedList(StructureElement):
    # Pandoc SHOULD only provide StructureElements here
    list_elements: List[List[Element]]


@dataclass
class UnorderedList(StructureElement):
    # Pandoc SHOULD only provide StructureElements here
    list_elements: List[List[Element]]


@dataclass
class Unprocessed(StructureElement):
    kind: str


# --- Text Elements -----------------------------------------------------------


@dataclass
class StyleElement(TextElement):
    # Pandoc SHOULD only provide TextElements/str here
    child: List[Element]


@dataclass
class Italic(StyleElement):
    pass


@dataclass
class Bold(StyleElement):
    pass


@dataclass
class CrossRef():
    identifier: str
    title: str


Note = object()
