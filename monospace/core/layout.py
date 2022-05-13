from typing import Dict, Iterator, List, Tuple, Type

from .domain import Settings
from .domain import blocks as b
from .formatting import Formatter
from .rendering import paragraph as p

# Left side: list of main lines
# Right side, dict for the side notes: desired offset, line
Page = Tuple[List[str], Dict[int, str]]
RenderedPage = List[str]


def layout(
    blocks: Iterator[b.Block],
    settings: Settings,
    formatter: Type[Formatter],
    linear=False,
) -> Iterator[RenderedPage]:

    s = settings
    content_length = s.page_height - s.margin_top - s.margin_bottom

    pages = break_blocks(blocks, linear, content_length, s.margin_top)
    rendered_pages = render_pages(pages, linear, s, formatter)

    return rendered_pages


def break_blocks(blocks, linear, content_length, margin_top) -> Iterator[Page]:
    latest_side_offset = 0
    first_page = True
    first_block = True
    current_page: Page = ([], {})

    def new_page():
        nonlocal latest_side_offset, current_page, first_block
        main = [""] * margin_top
        sides: Dict[int, str] = {}
        latest_side_offset = 0
        first_block = True
        current_page = (main, sides)

    new_page()

    # Prepare pages by breaking when there's not enough space
    # for either a block or its sides
    for block in blocks:
        block_size = len(block.main)
        sides_size = sum(len(s) for s in block.sides) + len(block.sides) - 1

        needed_main = block_size + block.block_offset
        needed_sides = sides_size + block.block_offset
        needed = max(needed_main, needed_sides)

        occupied = len(current_page[0])
        manual_page_break = not block.main and not block.sides

        # Don't break into pages when in linear mode
        if not linear:
            if (
                content_length - occupied < needed
                or manual_page_break
                or block.break_before and not first_page
            ):
                yield current_page
                new_page()
                if manual_page_break:
                    continue

        first_page = False

        # If we're at the beginning of the page, we don't need to offset block
        if not first_block:
            for _ in range(block.block_offset):
                current_page[0].append("")

        i = max(len(current_page[0]), latest_side_offset)
        current_page[0].extend(block.main)
        if block.sides:
            for side in block.sides:
                for line in side:
                    current_page[1][i] = line
                    i += 1
                i += 1  # Gap to separate sides from each other
        latest_side_offset = i

        first_block = False

    yield current_page


def render_pages(
    pages,
    linear,
    settings,
    formatter
) -> Iterator[RenderedPage]:

    s = settings
    ft = formatter.format_tags

    page_nums = page_numbers(s)

    def spaces(width):
        return ft([width * " "], settings)

    # Go through pages and compose lines
    for i, page in enumerate(pages):
        main = page[0]
        sides = page[1]

        rendered_page = []

        margin_outside = spaces(s.margin_outside)
        margin_inside = spaces(s.margin_inside)
        spacing = spaces(s.side_spacing)
        empty_side_line = spaces(s.side_width)
        empty_line = spaces(s.main_width)

        highest_side_offset = max(sides.keys(), default=0) + 1
        main_height = len(main)

        for j in range(max(main_height, highest_side_offset)):
            line = ""
            if j < main_height:
                line = main[j]
            if not line:
                line = empty_line

            side_line = empty_side_line
            if j in sides:
                side_line = sides[j]

            if i % 2 == 0:
                rendered_page.append(
                    margin_outside + side_line + spacing
                    + line + margin_inside
                )
            else:
                rendered_page.append(
                    margin_inside + line
                    + spacing + side_line + margin_outside
                )

        lines_left = s.page_height - (j + 1)

        if linear:
            # In linear mode, the only one page is longer than content_length
            lines_left = s.margin_bottom

        rendered_page.extend([spaces(settings.page_width)] * lines_left)

        # Insert page numbers post-rendering
        rendered_page[-3] = ft(next(page_nums), settings)

        yield rendered_page


def page_numbers(settings: Settings) -> Iterator[List[str]]:
    """
    Infinitely generate page numbers
    """
    i = 0
    while True:
        aligned = p.align(
            text_elements=[str(i)],
            alignment=p.Alignment.left if i % 2 == 0 else p.Alignment.right,
            width=settings.main_width + settings.side_spacing + settings.side_width,
        )[0]
        outside = " " * settings.margin_outside
        inside = " " * settings.margin_inside
        if i % 2 == 0:
            yield [outside, aligned, inside]
        else:
            yield [inside, aligned, outside]
        i += 1
