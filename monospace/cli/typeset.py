import logging
import os
import pathlib
import subprocess
import sys
import webbrowser
from pathlib import Path

import click
from leet.logging import log

from ..core import typeset as do_typeset
from ..core.formatting import AnsiFormatter, HtmlFormatter, PostScriptFormatter
from ..util import concatenate_markdown_directory

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
@click.option(
    "-l", "--linear",
    is_flag=True, default=False,
    help="Produce only one long page."
)
@click.option(
    "-v", "--verbose",
    count=True,
    help="Enable logging (-v: info, -vv: debug)"
)
def typeset(markdown_file, to, preview, do_open, linear, verbose):
    """Typeset a markdown file into a book.

    Saves the formatted book in the same directory as the input file.

    If the MARKDOWN_FILE argument is a path, all contained markdown files will
    be concatenated before typesetting (in alphabetical order.)
    """

    log_level = logging.WARNING
    if verbose == 1:
        log_level = logging.INFO
    elif verbose >= 2:
        log_level = logging.DEBUG
    log.setLevel(log_level)

    if os.path.isdir(markdown_file):
        output = os.path.join(markdown_file, os.path.split(markdown_file)[-1])
        working_dir = Path(markdown_file)
        content = concatenate_markdown_directory(markdown_file)
    else:
        output = markdown_file.rsplit(".md", 1)[0]
        working_dir = Path(markdown_file).parent
        with open(markdown_file, "r") as f:
            content = f.read()

    formatter = formatters[to]

    if preview:
        if to == "pdf":
            raise click.UsageError(
                "Option --preview is not available with format 'pdf'")
        output = sys.stdout

    do_typeset(
        markdown_content=content,
        output=output,
        working_dir=working_dir,
        formatter=formatter,
        linear=linear
    )

    if to == "pdf":
        subprocess.check_call(["ps2pdf", output + ".ps", output + ".pdf"])

    if do_open and not preview:
        path = os.path.abspath("%s.%s" % (output, to))
        uri = pathlib.Path(path).as_uri()
        webbrowser.open(uri)
