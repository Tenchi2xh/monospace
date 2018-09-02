import sys
import click
from .. import core
from ..core.domain import Settings
from ..core.formatting import AnsiFormatter, HtmlFormatter, PostScriptFormatter

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

formatters = {
    "ansi": AnsiFormatter,
    "html": HtmlFormatter,
    "ps": PostScriptFormatter
}


@click.command()
@click.argument(
    "markdown_file",
    type=click.Path(exists=True), required=True)
@click.option(
    "-t", "--to",
    type=click.Choice(formatters.keys()), required=True,
    help="Destination format.")
def typeset(markdown_file, to):
    """Typeset MARKDOWN_FILE into a book"""
    formatter = formatters[to]

    ast = core.parse(markdown_file)
    references, elements = core.process(ast)
    blocks = core.render(elements, settings, references, formatter=formatter)
    pages = core.layout(blocks, settings, formatter)

    formatter.write_file(sys.stdout, pages, settings)
