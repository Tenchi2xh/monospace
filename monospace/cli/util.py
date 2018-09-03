from .. import core
from ..core.formatting import PostScriptFormatter


def do_typeset(markdown_file, formatter, output):
    if formatter == PostScriptFormatter:
        from ..core.symbols import characters
        characters.small_caps["Q"] = characters.small_cap_q

    ast = core.parse(markdown_file)
    settings, references, elements = core.process(ast, markdown_file)
    blocks = core.render(elements, settings, references, formatter=formatter)
    pages = core.layout(blocks, settings, formatter)
    formatter.write_file(output, pages, settings)
