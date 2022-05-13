from dataclasses import dataclass, field
from typing import List, Optional, Union


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
    identifier: str


@dataclass
class SubChapter(StructureElement):
    title: Text
    subtitle: Text
    identifier: str


@dataclass
class Section(StructureElement):
    title: Text
    identifier: str


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
    caption: Element
    palette: Optional[str] = None
    mode: Optional[str] = None


@dataclass
class PageBreak(StructureElement):
    pass


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


@dataclass
class Anchor(TextElement):
    identifier: str


@dataclass
class Note(TextElement):
    count: Optional[int]


@dataclass
class Space:
    count: int = 1

    def __repr__(self):
        return "_"
