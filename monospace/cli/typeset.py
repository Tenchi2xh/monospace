import sys
import click
from ..core.formatting import AnsiFormatter, HtmlFormatter, PostScriptFormatter
from .util import do_typeset, dummy_settings


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
    do_typeset(markdown_file, formatter, dummy_settings, sys.stdout)
