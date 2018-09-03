import os
import sys
import click
import pathlib
import subprocess
import webbrowser

from ..core.formatting import AnsiFormatter, HtmlFormatter, PostScriptFormatter
from .util import do_typeset


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
    "-p", "--preview", "preview",
    is_flag=True, default=False,
    help="Do not save a file, just print to stdout."
)
@click.option(
    "-O", "--open", "do_open",
    is_flag=True, default=False,
    help="Open output file."
)
def typeset(markdown_file, to, preview, do_open):
    """Typeset a markdown file into a book.

    Saves the formatted book in the same directory as the input file.
    """
    filename = markdown_file.rsplit(".md", 1)[0]
    formatter = formatters[to]

    if preview:
        if to == "pdf":
            raise click.UsageError(
                "Option --preview is not available with format 'pdf'")
        filename = sys.stdout

    do_typeset(markdown_file, formatter, filename)

    if to == "pdf":
        subprocess.check_call(["ps2pdf", filename + ".ps", filename + ".pdf"])

    if do_open and not preview:
        path = os.path.abspath("%s.%s" % (filename, to))
        uri = pathlib.Path(path).as_uri()
        webbrowser.open(uri)
