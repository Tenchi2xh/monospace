import sys
import click
import subprocess
from ..core.formatting import AnsiFormatter, HtmlFormatter, PostScriptFormatter
from .util import do_typeset, dummy_settings


formatters = {
    "ansi": AnsiFormatter,
    "html": HtmlFormatter,
    "ps": PostScriptFormatter,
    "pdf": PostScriptFormatter,
}


@click.command()
@click.argument(
    "markdown_file",
    type=click.Path(exists=True), required=True)
@click.option(
    "-t", "--to",
    type=click.Choice(formatters.keys()), required=True,
    help="Destination format.")
@click.option(
    "-p", "--print", "do_print",
    is_flag=True, default=False,
    help="Do not save a file, print to stdout."
)
def typeset(markdown_file, to, do_print):
    """Typeset MARKDOWN_FILE into a book.

    Saves the formatted book in the same directory as the input file.
    """
    filename = markdown_file.rsplit(".md", 1)[0]
    formatter = formatters[to]

    if do_print:
        if to == "pdf":
            raise click.UsageError(
                "Option --print is not available with format 'pdf'")
        filename = sys.stdout

    do_typeset(markdown_file, formatter, dummy_settings, filename)

    if to == "pdf":
        subprocess.check_call(["ps2pdf", filename + ".ps", filename + ".pdf"])
