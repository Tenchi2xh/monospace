from typing import List, Union, TypeVar
from dataclasses import dataclass, field

class TextElement:
    pass

class StructureElement:
    pass

Words = List[str]
TextElementChild = Union[TextElement, Words]

# --- Structure Elements ------------------------------------------------------

TextType = TypeVar('Text')

@dataclass
class Text(StructureElement):
    elements: List[Union[TextElement, str]]
    notes: List[TextType] = field(default_factory=list)

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
    elements: List[StructureElement]

@dataclass
class UnorderedList(StructureElement):
    elements: List[StructureElement]

# --- Text Elements -----------------------------------------------------------

@dataclass
class StyleElement(TextElement):
    child: TextElementChild

@dataclass
class Italic(StyleElement): pass

@dataclass
class Bold(StyleElement): pass

@dataclass
class CrossRef():
    identifier: str
    title: str

Note = object()
