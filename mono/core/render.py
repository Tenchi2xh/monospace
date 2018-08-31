from typing import Dict, List
from .domain import document as d
from .domain import blocks as b
from .domain import Settings

"""Split a document into granular rendered blocks

Render all elements of a document and produce blocks.
Blocks indicate where a page can break, for example:

An OrderedList with two list entries,
each having two paragraphs of their own,
should produce 4 rendered blocks.

Each block has two parts: a main part, and a side part.
The side part will be set in the margin by the main renderer.
A side part contains:

- Sub-chapter headers with their subtitle
- Footnotes
- Figure, code blocks and table captions

Each of these side-elements are associated with an offset,
indicating at which line of the main part they were encountered.
An algorithm will spread them out in the side block,
trying as much as possible to put them near their desired offset.

Blocks also contain two offset values:

- The block offset tells the main renderer how many spaces to put
  relative to the previous set block. For example, new sub-chapters
  should have a block offset of 3, to leave some space after the
  previous section. Chapters have a block offset of -3: the main
  renderer will only put a chapter at the beginning of a page,
  and the title of the chapter will start above the line where
  normal paragraphs start.
- The side offset tells the main renderer where to place the side block
  _relative_ to the main block. This is mainly for sub-chapters, which
  have a horizontal line above the title that should not be placed
  at the same height as the text of the main block.

Side blocks are rendered without padding and alignment:
it is delegated to the main renderer, because the side blocks
need to be aligned left or right depending on which page they are on.
"""


def render(
    elements: List[d.Element],
    settings: Settings,
    cross_references: Dict[str, str]
) -> List[b.Block]:
    renderer = Renderer(elements, settings, cross_references)
    return renderer.blocks


class Renderer(object):
    def __init__(self, elements, settings, cross_references):
        self.settings: Settings = settings
        self.cross_references: Dict[str, str] = cross_references
        self.blocks = self.render_elements(elements)

    def render_elements(self, elements) -> List[b.Block]:
        blocks: List[b.Block] = []
        for element in elements:
            if isinstance(element, d.Chapter):
                blocks.append(self.render_chapter(element))
            if isinstance(element, d.SubChapter):
                pass
            if isinstance(element, d.Section):
                pass
            if isinstance(element, d.Paragraph):
                pass
            if isinstance(element, d.Quote):
                pass
            if isinstance(element, d.OrderedList):
                pass
            if isinstance(element, d.UnorderedList):
                pass
            if isinstance(element, d.Unprocessed):
                pass
        return blocks

    def render_chapter(self, chapter):
        pass