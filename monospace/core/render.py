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
            elif isinstance(element, d.Quote):
                blocks.append(self.render_quote(element))
            elif isinstance(element, d.PageBreak):
                blocks.append(b.Block())

            # Unimplemented:
            elif (
                isinstance(element, d.SubChapter)
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

        def decorated_indent(n):
            spaces = " " * self.settings.tab_size
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
            return self.format(result)

        for i, elements in enumerate(ordered_list.list_elements):
            sub_blocks = renderer.render_elements(elements)

            for j, block in enumerate(sub_blocks):
                decorated = decorated_indent(i) if j == 0 else None
                block.main = self.indent(
                    lines=block.main,
                    left_width=4,
                    right_width=0,
                    before=decorated
                )

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
        lines.append(self.format([" " * self.settings.main_width]))

        # TODO: Notes
        return b.Block(main=lines)

    def render_subchapter(self, subchapter):
        line = ["━" * self.settings.side_width]
        formatted_line = self.format(line)

        title = [d.Bold(subchapter.title.elements)]
        title_lines = p.align(
            text_elements=title,
            alignment=p.Alignment.left,
            width=self.settings.side_width,
            format_func=self.format
        )

        side = [formatted_line] + title_lines

        if subchapter.subtitle:
            subtitle = [d.Italic(subchapter.subtitle.elements)]
            subtitle_lines = p.align(
                text_elements=subtitle,
                alignment=p.Alignment.left,
                width=self.settings.side_width,
                format_func=self.format
            )
            space = self.format([" " * self.settings.side_width])
            side += [space] + subtitle_lines

        return b.Block(sides=[side])

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
            alignment=p.Alignment.justify,
            width=self.settings.main_width,
            format_func=self.format
        )

        # TODO: Notes
        return b.Block(main=lines)

    def render_aside(self, aside):
        # Note: although aside is composed of multiple blocks,
        # we want to only return one block, because aside shouldn't be broken

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

        fence = ft(["─" * width])
        empty_line = ft([" " * main_width])

        renderer = self.get_subrenderer(main_width=width)
        blocks = renderer.render_elements(aside.elements)

        lines = []
        for block in blocks:
            for line in block.main:
                lines.append(line)
            lines.append(empty_line)
        lines.pop()

        # TODO: Notes
        return b.Block(main=self.indent(
            lines=lines,
            left_width=tab_size, right_width=tab_size,
            top_line=fence, bottom_line=fence,
            inner_tags=[color]
        ))

    def render_quote(self, quote):
        tab_size = self.settings.tab_size
        content_width = self.settings.main_width - tab_size * 2

        elements = quote.text.elements

        author_lines = []
        if isinstance(elements[-1], d.Bold):
            author = ["—", d.space] + elements.pop().children
            author_lines = p.align(
                text_elements=author,
                alignment=p.Alignment.right,
                width=content_width,
                format_func=self.format
            )

        lines = p.align(
            text_elements=[d.Italic(elements)],
            alignment=p.Alignment.center,
            width=content_width,
            format_func=self.format
        )

        empty_line = self.format(" " * content_width)

        return b.Block(main=self.indent(
            lines=lines + [empty_line] + author_lines,
            left_width=tab_size, right_width=tab_size,
        ))

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
        for i in range(len(highlighted)):
            highlighted[i] = ft(["  "]) + highlighted[i] + ft(["  "])

        bg = FormatTag(kind=F.BackgroundColor, data={"color": "#222222"})
        if self.settings.light:
            bg.data["color"] = "#eeeeee"

        fence_color = dark_gray
        if self.settings.light:
            fence_color = light_gray

        top = ft([fence_color, "▔" * (mw - ts * 2), fence_color.close_tag])
        bottom = ft([fence_color, "▁" * (mw - ts * 2), fence_color.close_tag])

        return b.Block(main=self.indent(
            lines=highlighted,
            left_width=ts, right_width=ts,
            top_line=top, bottom_line=bottom,
            inner_tags=[bg]
        ))

    def render_image(self, image):
        extension = image.uri.rsplit(".", 1)[-1]
        cwd = os.path.dirname(self.settings.source_file)
        real_uri = os.path.join(cwd, image.uri)

        if extension in ("png", "jpg", "jpeg"):
            width = self.settings.main_width - 2 * self.settings.tab_size
            mode = images.Mode.Pixels
            if image.mode is not None:
                mode = images.Mode[image.mode]
            palette = images.Palette.RGB
            if image.palette is not None:
                palette = images.Palette[image.palette]

            image_lines = images.ansify(
                real_uri,
                format_func=self.format,
                width=width,
                mode=mode,
                palette=palette,
            )

            # TODO: Caption
            return b.Block(main=self.indent(
                lines=image_lines,
                left_width=self.settings.tab_size,
                right_width=self.settings.tab_size))
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

    def indent(
        self,
        lines: List[str],
        left_width: int,
        right_width: int,
        top_line: Optional[str]=None,
        bottom_line: Optional[str]=None,
        before: Optional[str]=None,
        after: Optional[str]=None,
        outer_tags: Optional[List[FormatTag]]=None,
        inner_tags: Optional[List[FormatTag]]=None,
    ):
        """
        Indents a list of lines with the following format:

            ....TTTTTTTTTT....    T: Top line
            bbbbllllllllll....    b: before
            ....llllllllll....    l: lines
            ....llllllllllaaaa    b: after
            ....BBBBBBBBBB....    B: Bottom line

        Note: lines are expected to be all the same width
        """
        ft = self.format
        result = []

        open_outer = [] if outer_tags is None else outer_tags
        close_outer = [tag.close_tag for tag in open_outer]
        open_inner = [] if inner_tags is None else inner_tags
        close_inner = [tag.close_tag for tag in open_inner]

        left_indent = ft([*open_outer, " " * left_width, *open_inner])
        right_indent = ft([*close_inner, " " * right_width, *close_outer])

        if before:
            before = ft(open_outer) + before + ft(open_inner)

        if after:
            after = ft(close_inner) + after + ft(close_outer)

        if top_line:
            top_line = left_indent + top_line + right_indent
            result.append(top_line)

        for i, line in enumerate(lines):
            left = before if before and i == 0 else left_indent
            right = after if after and i == len(lines) - 1 else right_indent
            result.append(left + line + right)

        if bottom_line:
            bottom_line = left_indent + bottom_line + right_indent
            result.append(bottom_line)

        return result

    def format(self, elems):
        return self.formatter.format_tags(elems, self.settings)


light_gray = FormatTag(kind=F.ForegroundColor, data={"color": "#aaaaaa"})
mid_gray = FormatTag(kind=F.ForegroundColor, data={"color": "#888888"})
dark_gray = FormatTag(kind=F.ForegroundColor, data={"color": "#444444"})
