from typing import Dict, List, Optional, Type
from dataclasses import replace

from .domain import document as d
from .domain import blocks as b
from .domain import Settings
from .rendering import paragraph as p
from .formatting import Formatter, styles

"""Split a document into granular rendered blocks

Render all elements of a document and produce blocks.
Blocks indicate where a page can break, for example:

    An OrderedList with two list entries,
    each having two paragraphs of their own,
    should produce 4 rendered blocks.

Every Block has two parts: a main part, and a side part.
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
    cross_references: Dict[str, str],
    formatter: Optional[Type[Formatter]] = None
) -> List[b.Block]:
    renderer = Renderer(settings, cross_references, formatter)
    return renderer.render_elements(elements)


class Renderer(object):
    def __init__(self, settings, cross_references, formatter=None):
        self.settings: Settings = settings
        self.cross_references: Dict[str, str] = cross_references
        self.formatter = formatter

    def render_elements(self, elements) -> List[b.Block]:
        blocks: List[b.Block] = []
        for element in elements:
            if isinstance(element, d.Chapter):
                blocks.append(self.render_chapter(element))
            if isinstance(element, d.SubChapter):
                pass
            if isinstance(element, d.Section):
                blocks.append(self.render_section(element))
            if isinstance(element, d.Paragraph):
                blocks.append(self.render_paragraph(element))
            if isinstance(element, d.Quote):
                pass
            if isinstance(element, d.OrderedList):
                blocks.extend(self.render_list(element, ordered=True))
            if isinstance(element, d.UnorderedList):
                blocks.extend(self.render_list(element, ordered=False))
            if isinstance(element, d.Unprocessed):
                pass
        return blocks

    def render_list(self, ordered_list, ordered=False):
        blocks = []

        # Create sub-renderer that will create thinner blocks
        renderer = Renderer(
            settings=replace(
                self.settings,
                page_width=self.settings.page_width - self.settings.tab_size
            ),
            cross_references=self.cross_references,
            formatter=self.formatter
        )

        # Render all list entries and indent them
        # If sub-renderers also render nested lists, they will indent them
        # so the indentation adds up, no need to count levels :)

        # TODO: Add bullets/numbers

        for i, elements in enumerate(ordered_list.list_elements):
            sub_blocks = renderer.render_elements(elements)

            indent = " " * self.settings.tab_size
            for block in sub_blocks:
                for j, line in enumerate(block.main):
                    block.main[j] = indent + line

            # Decorate
            bullet = "•"
            if ordered:
                bullet = styles.circled(i)
            first_line = sub_blocks[0].main[0]
            decorated_line = bullet + first_line[len(bullet):]
            sub_blocks[0].main[0] = decorated_line

            blocks.extend(sub_blocks)

        return blocks

    def render_chapter(self, chapter):
        elements = [d.Bold([d.Italic(chapter.title.elements)])]

        lines = p.align(
            text_elements=elements,
            alignment=p.Alignment.left,
            width=self.settings.main_width,
            formatter=self.formatter
        )
        lines.insert(0, "━" * self.settings.main_width)

        # TODO: Notes
        return b.Block(main=lines, block_offset=-2)

    def render_section(self, section):
        elements = [d.Bold(section.title.elements)]

        lines = p.align(
            text_elements=elements,
            alignment=p.Alignment.left,
            width=self.settings.main_width,
            formatter=self.formatter,
            text_filter=styles.small_caps
        )

        # TODO: Notes
        return b.Block(main=lines)

    def render_paragraph(self, paragraph):
        lines = p.align(
            text_elements=paragraph.text.elements,
            alignment=p.Alignment.left,
            width=self.settings.main_width,
            formatter=self.formatter
        )

        # TODO: Notes
        return b.Block(main=lines)
