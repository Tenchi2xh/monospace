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

import os
from dataclasses import replace
from typing import Dict, Iterator, List, Optional, Type

from leet.logging import log, log_progress

from .domain import Settings
from .domain import blocks as b
from .domain import document as d
from .formatting import AnsiFormatter
from .formatting import Format as F
from .formatting import FormatTag, Formatter, PostScriptFormatter, styles
from .rendering import code, images
from .rendering import paragraph as p
from .symbols import characters


def render(
    elements: Iterator[d.Element],
    settings: Settings,
    cross_references: Dict[str, str],
    formatter: Optional[Type[Formatter]] = None
) -> Iterator[b.Block]:
    renderer = Renderer(settings, cross_references, formatter)
    log.info("Rendering domain elements into string blocks...")
    return renderer.render_elements(elements, progress=True)


class Renderer(object):
    def __init__(self, settings, cross_references, formatter=None):
        self.settings: Settings = settings
        self.cross_references: Dict[str, str] = cross_references
        self.formatter = formatter

    def render_elements(self, elements, progress=False) -> Iterator[b.Block]:
        if progress:
            elements = log_progress.debug(elements)

        for element in elements:
            name = element.__class__.__name__

            def pb(block):
                if name in self.settings.break_before:
                    (block[0] if isinstance(block, list) else block).break_before = True
                return block

            if isinstance(element, d.Chapter):
                yield pb(self.render_chapter(element))
            elif isinstance(element, d.SubChapter):
                yield pb(self.render_subchapter(element))
            elif isinstance(element, d.Section):
                yield pb(self.render_section(element))
            elif isinstance(element, d.Paragraph):
                yield pb(self.render_paragraph(element))
            elif isinstance(element, d.OrderedList):
                yield from pb(self.render_list(element, ordered=True))
            elif isinstance(element, d.UnorderedList):
                yield from pb(self.render_list(element, ordered=False))
            elif isinstance(element, d.Aside):
                yield pb(self.render_aside(element))
            elif isinstance(element, d.CodeBlock):
                yield pb(self.render_code_block(element))
            elif isinstance(element, d.Image):
                yield pb(self.render_image(element))
            elif isinstance(element, d.Quote):
                yield pb(self.render_quote(element))
            elif isinstance(element, d.PageBreak):
                yield b.Block()

            # Unimplemented:
            elif (
                isinstance(element, d.SubChapter)
                or isinstance(element, d.Unprocessed)
            ):
                if isinstance(element, d.Unprocessed):
                    kind = element.kind
                else:
                    kind = element.__class__.__name__

                yield self.render_paragraph(
                    d.Paragraph(text=d.Text(["<UNRENDERED: %s>" % kind]))
                )

    def render_list(self, ordered_list, ordered=False):
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
                yield block

    def render_chapter(self, chapter):
        elements, notes = self.render_notes(chapter.title.elements)
        title = [
            d.Anchor(
                [d.Bold([d.Italic(elements)])],
                identifier=chapter.identifier
            )
        ]

        lines = p.align(
            text_elements=title,
            alignment=p.Alignment.left,
            width=self.settings.main_width,
            format_func=self.format
        )
        fence = ["━" * self.settings.main_width]
        lines.insert(0, self.format(fence))
        lines.append(self.format([" " * self.settings.main_width]))

        return b.Block(main=lines, sides=notes)

    def render_subchapter(self, subchapter):
        elements, notes = self.render_notes(subchapter.title.elements)
        line = ["━" * self.settings.side_width]
        formatted_line = self.format(line)

        title = [
            d.Anchor([d.Bold(elements)], identifier=subchapter.identifier)
        ]
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

        return b.Block(sides=[side] + notes)

    def render_section(self, section):
        elements, notes = self.render_notes(section.title.elements)
        title = [d.Anchor([d.Bold(elements)], identifier=section.identifier)]

        lines = p.align(
            text_elements=title,
            alignment=p.Alignment.left,
            width=self.settings.main_width,
            format_func=self.format,
            text_filter=styles.small_caps
        )

        return b.Block(main=lines, sides=notes)

    def render_notes(self, elements):
        new_elements = []
        notes = []

        # TODO: Put this in Theme object
        color = light_gray
        if self.settings.light:
            color = mid_gray

        def gray_format(elems):
            return self.format([color, *elems, color.close_tag])

        for elem in elements:
            if isinstance(elem, d.Note):
                counter = []
                if elem.count is not None:
                    sup = styles.number_map2(
                        str(elem.count), characters.superscript)
                    new_elements.append(sup)
                    counter = [sup + ":", d.Space()]
                side = [d.Italic(counter + [*elem.children])]
                notes.append(p.align(
                    text_elements=side,
                    alignment=p.Alignment.left,
                    width=self.settings.side_width,
                    format_func=gray_format
                ))
            else:
                new_elements.append(elem)
        return new_elements, notes

    def render_paragraph(self, paragraph):
        elements, notes = self.render_notes(paragraph.text.elements)
        lines = p.align(
            text_elements=elements,
            alignment=p.Alignment.justify,
            width=self.settings.main_width,
            format_func=self.format
        )

        return b.Block(main=lines, sides=notes)

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
        blocks = list(renderer.render_elements(aside.elements))
        notes = [side for block in blocks for side in block.sides]

        lines = []
        for block in blocks:
            for line in block.main:
                lines.append(line)
            lines.append(empty_line)
        lines.pop()

        return b.Block(
            main=self.indent(
                lines=lines,
                left_width=tab_size, right_width=tab_size,
                top_line=fence, bottom_line=fence,
                inner_tags=[color]
            ),
            sides=notes
        )

    def render_quote(self, quote):
        tab_size = self.settings.tab_size
        content_width = self.settings.main_width - tab_size * 2

        elements = quote.text.elements

        author_lines = []
        if isinstance(elements[-1], d.Bold):
            author = ["—", d.Space()] + elements.pop().children
            author_lines = p.align(
                text_elements=author,
                alignment=p.Alignment.right,
                width=content_width,
                format_func=self.format
            )

        elements, notes = self.render_notes(elements)

        lines = p.align(
            text_elements=[d.Italic(elements)],
            alignment=p.Alignment.center,
            width=content_width,
            format_func=self.format
        )

        empty_line = self.format(" " * content_width)

        return b.Block(
            main=self.indent(
                lines=lines + [empty_line] + author_lines,
                left_width=tab_size, right_width=tab_size,
            ),
            sides=notes
        )

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
        real_uri = os.path.join(self.settings.working_dir, image.uri)

        sides = []
        if image.caption:
            sides = self.render_notes([image.caption])[1]

        if extension in ("png", "jpg", "jpeg"):
            image_width, _ = images.dimensions(real_uri)
            if image_width > self.settings.main_width:
                width = self.settings.main_width - 2 * self.settings.tab_size
                margin = self.settings.tab_size
            else:
                width = image_width
                margin = 0

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

            return b.Block(
                main=self.indent(
                    lines=image_lines,
                    left_width=margin,
                    right_width=margin
                ),
                sides=sides,
            )
        else:
            with open(real_uri, "r") as f:
                lines = f.read().splitlines()

            max_length = max(len(line) for line in lines)
            if max_length > self.settings.main_width:
                raise RuntimeError(
                    "Image '%s' is too wide: length %d is higher than %d"
                    % (real_uri, max_length, self.settings.main_width)
                )

            padded_lines = [line.ljust(max_length) for line in lines]
            formatted_lines = [self.format(line) for line in padded_lines]
            left_indent = (self.settings.main_width - max_length) // 2
            right_indent = self.settings.main_width - max_length - left_indent

            return b.Block(
                main=self.indent(
                    lines=formatted_lines,
                    left_width=left_indent,
                    right_width=right_indent,
                ),
                sides=sides,
            )

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
        top_line: Optional[str] = None,
        bottom_line: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        outer_tags: Optional[List[FormatTag]] = None,
        inner_tags: Optional[List[FormatTag]] = None,
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
