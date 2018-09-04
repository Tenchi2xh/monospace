from typing import Type, List, Tuple, Dict

from .domain import Settings, blocks as b
from .formatting import Formatter


def layout(
    blocks: List[b.Block],
    settings: Settings,
    formatter: Type[Formatter]
):

    # Left side: list of main lines
    # Right side, dict for the side notes: desired offset, line
    Page = Tuple[List[str], Dict[int, str]]
    pages: List[Page] = []

    s = settings
    content_length = s.page_height - s.margin_top - s.margin_bottom

    def new_page():
        main = [""] * s.margin_top
        sides = {}
        pages.append((main, sides))

    new_page()
    current_page = pages[-1]

    # TODO: add "break_before: bool" to block for chapters
    # (only break if occupied = 0)

    # Prepare pages by breaking when there's not enough space
    # for either a block or its sides
    for block in blocks:
        block_size = len(block.main)
        sides_size = sum(len(s) for s in block.sides) + len(block.sides) - 1

        needed_main = block_size + block.block_offset
        needed_sides = sides_size + block.block_offset
        needed = max(needed_main, needed_sides)

        occupied = len(current_page[0])
        if content_length - occupied < needed:
            new_page()
            current_page = pages[-1]

        # If we're at the beginning of the page, we don't need to offset block
        if len(current_page[0]) != 0:
            for _ in range(block.block_offset):
                current_page[0].append("")

        i = len(current_page[0])
        current_page[0].extend(block.main)
        if block.sides:
            for side in block.sides:
                for line in side:
                    current_page[1][i] = line
                    i += 1
                i += 1  # Gap to separate sides from each other

    rendered_pages: List[List[str]] = []
    ft = formatter.format_tags

    def spaces(width):
        return ft([width * " "], settings)

    # Go through pages and compose lines
    # FIXME: Current implementation may put side notes on top of each other
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
        print(sides, highest_side_offset, main_height)

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

        lines_left = s.margin_bottom + (content_length - j)
        rendered_page.extend([spaces(settings.page_width)] * lines_left)

        rendered_pages.append(rendered_page)

    return rendered_pages
