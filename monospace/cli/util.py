from .. import core
from ..core.domain import Settings
from ..core.formatting import PostScriptFormatter

dummy_settings = Settings(
    main_width=70,
    side_width=20,
    page_height=60,

    side_spacing=4,
    tab_size=4,

    margin_top=5,
    margin_inside=10,
    margin_outside=5,
    margin_bottom=5
)


def do_typeset(markdown_file, formatter, settings, output):
    if formatter == PostScriptFormatter:
        from ..core.symbols import characters
        characters.small_caps["Q"] = characters.small_cap_q

    ast = core.parse(markdown_file)
    references, elements = core.process(ast)
    blocks = core.render(elements, settings, references, formatter=formatter)
    pages = core.layout(blocks, settings, formatter)
    formatter.write_file(output, pages, settings)
