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
import os

from .domain import document as d
from .domain import blocks as b
from .domain import Settings
from .rendering import paragraph as p, code, images
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
            elif isinstance(element, d.SubChapter):
                blocks.append(self.render_subchapter(element))
            elif isinstance(element, d.Section):
                blocks.append(self.render_section(element))
            elif isinstance(element, d.Paragraph):
                blocks.append(self.render_paragraph(element))
            elif isinstance(element, d.OrderedList):
                blocks.extend(self.render_list(element, ordered=True))
            elif isinstance(element, d.UnorderedList):
                blocks.extend(self.render_list(element, ordered=False))
            elif isinstance(element, d.Aside):
                blocks.append(self.render_aside(element))
            elif isinstance(element, d.CodeBlock):
                blocks.append(self.render_code_block(element))
            elif isinstance(element, d.Image):
                blocks.append(self.render_image(element))

            # Unimplemented:
            elif (
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
                    formatted_indent = self.format([indent])
                    block.main[k] = formatted_indent + line

            blocks.extend(sub_blocks)

        return blocks

    def render_chapter(self, chapter):
        elements = [d.Bold([d.Italic(chapter.title.elements)])]

        lines = p.align(
            text_elements=elements,
            alignment=p.Alignment.left,
            width=self.settings.main_width,
            format_func=self.format
        )
        fence = ["━" * self.settings.main_width]
        lines.insert(0, self.format(fence))

        # TODO: Notes
        return b.Block(main=lines)

    def render_subchapter(self, subchapter):
        line = ["━" * self.settings.side_width]
        title = [d.Bold(subchapter.title.elements)]
        subtitle = [d.Italic(subchapter.subtitle.elements)]

        formatted_line = self.format(line)
        title_lines = p.align(
            text_elements=title,
            alignment=p.Alignment.left,
            width=self.settings.side_width,
            format_func=self.format
        )
        space = self.format([" " * self.settings.side_width])
        subtitle_lines = p.align(
            text_elements=subtitle,
            alignment=p.Alignment.left,
            width=self.settings.side_width,
            format_func=self.format
        )

        return b.Block(
            sides=[[formatted_line] + title_lines + [space] + subtitle_lines],
        )

    def render_section(self, section):
        elements = [d.Bold(section.title.elements)]

        lines = p.align(
            text_elements=elements,
            alignment=p.Alignment.left,
            width=self.settings.main_width,
            format_func=self.format,
            text_filter=styles.small_caps
        )

        # TODO: Notes
        return b.Block(main=lines)

    def render_paragraph(self, paragraph):
        lines = p.align(
            text_elements=paragraph.text.elements,
            alignment=p.Alignment.left,
            width=self.settings.main_width,
            format_func=self.format
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
        ft = self.format

        width = main_width - 2 * tab_size

        color = light_gray
        if self.settings.light:
            color = mid_gray
        left_indent = ft([color, " " * tab_size])
        right_indent = ft([" " * tab_size, color.close_tag])
        fence = left_indent + ft(["─" * width]) + right_indent
        empty_line = ft([" " * main_width])

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
        ft = self.format
        ts = self.settings.tab_size
        mw = self.settings.main_width

        highlighted = code.highlight_code_block(
            code_block=code_block,
            format_func=self.format,
            # We want a tab size on each side,
            # plus a 2 characters for background
            width=(mw - ts * 2 - 4),
            light=self.settings.light
        )

        bg = FormatTag(kind=F.BackgroundColor, data={"color": "#222222"})
        if self.settings.light:
            bg.data["color"] = "#eeeeee"

        indent = " " * ts
        indent_left = ft([indent, bg, "  "])
        indent_right = ft(["  ", bg.close_tag, indent])

        for i, line in enumerate(highlighted):
            highlighted[i] = indent_left + line + indent_right

        fences = []
        fence_color = dark_gray
        if self.settings.light:
            fence_color = light_gray
        for char in ("▔", "▁"):
            fences.append(ft([
                indent,
                bg, fence_color,
                char * (mw - ts * 2),
                fence_color.close_tag, bg.close_tag,
                indent
            ]))
        highlighted.insert(0, fences[0])
        highlighted.append(fences[1])

        return b.Block(main=highlighted)

    def render_image(self, image):
        extension = image.uri.rsplit(".", 1)[-1]
        cwd = os.path.dirname(self.settings.source_file)
        real_uri = os.path.join(cwd, image.uri)

        if extension in ("png", "jpg", "jpeg"):
            # TODO: Attributes for level of detail
            width = self.settings.main_width - 2 * self.settings.tab_size
            image_lines = images.ansify(real_uri, self.format, width)
            indent = self.format(" " * self.settings.tab_size)
            indented = [
                indent + line + indent
                for line in image_lines
            ]

            # TODO: Caption
            return b.Block(main=indented)
        else:
            return b.Block(
                main=self.format(["<UNRENDERED: Image>"]))

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

    def format(self, elems):
        return self.formatter.format_tags(elems, self.settings)


light_gray = FormatTag(kind=F.ForegroundColor, data={"color": "#aaaaaa"})
mid_gray = FormatTag(kind=F.ForegroundColor, data={"color": "#888888"})
dark_gray = FormatTag(kind=F.ForegroundColor, data={"color": "#444444"})
