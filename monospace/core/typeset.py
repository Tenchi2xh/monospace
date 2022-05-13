from dataclasses import replace

from . import layout, parse, process, render
from .formatting import PostScriptFormatter


def typeset(markdown_content, output, working_dir, formatter, linear=False):
    # Somehow the real Small Cap Q symbol only displays nice in PostScript
    if formatter == PostScriptFormatter:
        from ..core.symbols import characters
        characters.small_caps["Q"] = characters.small_cap_q

    ast = parse(markdown_content)
    settings, references, elements = process(ast, working_dir)
    blocks = render(elements, settings, references, formatter=formatter)
    pages = layout(blocks, settings, formatter, linear=linear)

    if linear:
        pages = list(pages)
        settings = replace(
            settings,
            page_height=len(pages[0]) + settings.margin_bottom
        )

    formatter.write_file(output, pages, settings)
