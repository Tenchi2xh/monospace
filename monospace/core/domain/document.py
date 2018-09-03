from typing import List, Union
from dataclasses import dataclass, field


@dataclass
class TextElement:
    children: List["Element"]


class StructureElement:
    pass


TextElements = List[Union[TextElement, str]]


@dataclass
class Text:
    elements: TextElements
    notes: List["Text"] = field(default_factory=list)


Element = Union[StructureElement, TextElement, "Space", str]

# --- Structure Elements ------------------------------------------------------


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
class Aside(StructureElement):
    elements: List[Element]


@dataclass
class CodeBlock(StructureElement):
    language: str
    code: str


@dataclass
class Image(StructureElement):
    uri: str


@dataclass
class Unprocessed(StructureElement):
    kind: str


# --- Text Elements -----------------------------------------------------------


@dataclass
class Italic(TextElement):
    pass


@dataclass
class Bold(TextElement):
    pass


@dataclass
class CrossRef(TextElement):
    identifier: str


@dataclass
class Code(TextElement):
    pass


@dataclass
class Quoted(TextElement):
    pass


Note = object()


@dataclass
class Space:
    def __repr__(self):
        return "_"


space = Space()
