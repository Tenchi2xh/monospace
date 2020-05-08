from .. import core
from ..core.formatting import PostScriptFormatter
from dataclasses import replace


def do_typeset(markdown_file, formatter, output, linear=False):
    # Somehow the real Small Cap Q symbol only displays nice in PostScript
    if formatter == PostScriptFormatter:
        from ..core.symbols import characters
        characters.small_caps["Q"] = characters.small_cap_q

    ast = core.parse(markdown_file)
    settings, references, elements = core.process(ast, markdown_file)
    blocks = core.render(elements, settings, references, formatter=formatter)
    pages = core.layout(blocks, settings, formatter, linear=linear)

    if linear:
        settings = replace(
            settings,
            page_height=len(pages[0]) + settings.margin_bottom
        )

    formatter.write_file(output, pages, settings)
