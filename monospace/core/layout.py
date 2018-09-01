from typing import Type, List

from .domain import Settings, blocks as b
from .formatting import Formatter

settings = Settings(
    main_width=60,
    side_width=20,
    page_height=60,

    side_spacing=4,
    tab_size=4,

    margin_top=5,
    margin_inside=10,
    margin_outside=5,
    margin_bottom=5
)


def layout(
    blocks: List[b.Block],
    formatter: Type[Formatter]
):
    # For now, very basic laying out process, just for getting the cli started

    s = settings
    pages: List[List[str]] = [[]]

    def start_page():
        for i in range(s.margin_top):
            pages[-1].append(formatter.format_tags([" " * s.page_width]))

    content_length = s.page_height - s.margin_top - s.margin_bottom

    def indent():
        if len(pages) % 2 == 1:
            margin = s.margin_outside + s.side_width + s.side_spacing
        else:
            margin = s.margin_inside
        return formatter.format_tags([" " * margin])

    start_page()
    for block in blocks:
        for line in block.main:
            pages[-1].append(indent() + line)
            if len(pages[-1]) >= content_length:
                pages.append([])
                start_page()
        pages[-1].append("() u ")

    return pages
