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

from typing import Dict, List, Optional, Type
from dataclasses import replace

from .domain import document as d
from .domain import blocks as b
from .domain import Settings
from .rendering import paragraph as p, code
from .formatting import Formatter, styles, AnsiFormatter,\
                        PostScriptFormatter, FormatTag, Format as F


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
            if isinstance(element, d.Section):
                blocks.append(self.render_section(element))
            if isinstance(element, d.Paragraph):
                blocks.append(self.render_paragraph(element))
            if isinstance(element, d.OrderedList):
                blocks.extend(self.render_list(element, ordered=True))
            if isinstance(element, d.UnorderedList):
                blocks.extend(self.render_list(element, ordered=False))
            if isinstance(element, d.Aside):
                blocks.append(self.render_aside(element))
            if isinstance(element, d.CodeBlock):
                blocks.append(self.render_code_block(element))

            # Unimplemented:
            if (
                isinstance(element, d.SubChapter)
                or isinstance(element, d.Quote)
                or isinstance(element, d.Unprocessed)
            ):
                if isinstance(element, d.Unprocessed):
                    kind = element.kind
                else:
                    kind = element.__class__.__name__

                blocks.append(self.render_paragraph(
                    d.Paragraph(text=d.Text(["<UNRENDERED: %s>" % kind]))
                ))

        return blocks

    def render_list(self, ordered_list, ordered=False):
        blocks = []

        # Create sub-renderer that will create thinner blocks
        renderer = self.get_subrenderer(
            main_width=self.settings.main_width - self.settings.tab_size
        )

        # Render all list entries and indent them
        # If sub-renderers also render nested lists, they will indent them
        # so the indentation adds up, no need to count levels :)

        def decorate(spaces, n):
            bullet = "•"
            offset = 1
            if ordered:
                bullet = styles.circled(n)
                offset = 2  # Circled numbers are two characters wide...
                if self.formatter == AnsiFormatter and n <= 20:
                    # ...Unless you print them in a terminal and
                    # the number is <= 20? o_O
                    offset = 1
                if self.formatter == PostScriptFormatter:
                    offset = 1  # ps template has fixed offsets

            result = bullet + spaces[offset:]
            return result

        for i, elements in enumerate(ordered_list.list_elements):
            sub_blocks = renderer.render_elements(elements)

            for j, block in enumerate(sub_blocks):
                for k, line in enumerate(block.main):
                    indent = " " * self.settings.tab_size
                    if j == 0 and k == 0:
                        indent = decorate(indent, i)
                    formatted_indent = self.formatter.format_tags([indent])
                    block.main[k] = formatted_indent + line

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
        line_elements = ["━" * self.settings.main_width]
        formated_line = self.formatter.format_tags(line_elements)
        lines.insert(0, formated_line)

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

    def render_aside(self, aside):
        # Note: although aside is composed of multiple blocks,
        # we want to only return one block, because aside shouldn't be broken
        lines = []

        # Produce this:
        # ....────────....
        # ....(blocks)....
        # ....────────....
        #   ^          ^
        #   \ tab_size /

        main_width = self.settings.main_width
        tab_size = self.settings.tab_size
        f = self.formatter.format_tags

        width = main_width - 2 * tab_size

        gray = FormatTag(
            kind=F.ForegroundColor,
            data={"color": "#aaaaaa"}
        )

        left_indent = f([gray, " " * tab_size])
        right_indent = f([" " * tab_size, gray.close_tag])
        fence = left_indent + f(["─" * width]) + right_indent
        empty_line = f([" " * main_width])

        renderer = self.get_subrenderer(main_width=width)
        blocks = renderer.render_elements(aside.elements)

        lines.append(fence)
        for block in blocks:
            for line in block.main:
                lines.append(left_indent + line + right_indent)
            lines.append(empty_line)
        lines[-1] = fence

        # TODO: Notes
        return b.Block(main=lines)

    def render_code_block(self, code_block):
        ft = self.formatter.format_tags
        ts = self.settings.tab_size
        mw = self.settings.main_width

        highlighted = code.highlight_code_block(
            code_block=code_block,
            formatter=self.formatter,
            # We want a tab size on each side,
            # plus a 2 characters for background
            width=(mw - ts * 2 - 4),
        )

        bg = FormatTag(kind=F.BackgroundColor, data={"color": "#222222"})
        indent = " " * ts
        indent_left = ft([indent, bg, "  "])
        indent_right = ft(["  ", bg.close_tag, indent])

        for i, line in enumerate(highlighted):
            highlighted[i] = indent_left + line + indent_right

        spaces = ft([indent, bg, " " * (mw - ts * 2), bg.close_tag, indent])
        highlighted.insert(0, spaces)
        highlighted.append(spaces)

        return b.Block(main=highlighted)

    def get_subrenderer(self, main_width=None):
        return Renderer(
            settings=replace(
                self.settings,
                main_width=(
                    self.settings.main_width
                    if main_width is None
                    else main_width
                )
            ),
            cross_references=self.cross_references,
            formatter=self.formatter
        )
