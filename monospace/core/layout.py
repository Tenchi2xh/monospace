from typing import Type, List

from .domain import Settings, blocks as b
from .formatting import Formatter


def layout(
    blocks: List[b.Block],
    settings: Settings,
    formatter: Type[Formatter]
):
    # For now, very basic laying out process, just for getting the cli started

    s = settings
    pages: List[List[str]] = [[]]

    empty_line = formatter.format_tags([" " * s.page_width], settings)

    def start_page():
        for _ in range(s.margin_top):
            pages[-1].append(empty_line)

    content_length = s.page_height - s.margin_top - s.margin_bottom

    def indent(line):
        margin_left = s.margin_outside + s.side_width + s.side_spacing
        margin_right = s.margin_inside
        if len(pages) % 2 == 0:
            margin_left, margin_right = margin_right, margin_left
        return (
            formatter.format_tags([" " * margin_left], settings)
            + line
            + formatter.format_tags([" " * margin_right], settings)
        )

    start_page()
    for block in blocks:
        for line in block.main:
            pages[-1].append(indent(line))
            if len(pages[-1]) >= content_length:
                pages.append([])
                start_page()
        pages[-1].append(empty_line)

    return pages
