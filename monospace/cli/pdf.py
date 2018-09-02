import os
import click
import subprocess
from ..core.formatting import PostScriptFormatter
from .util import do_typeset, dummy_settings


@click.command()
@click.argument("markdown_file", type=click.Path(exists=True), required=True)
def pdf(markdown_file):
    """Generate a PDF book using MARKDOWN_FILE"""

    # TODO: Check if ghostscript is installed

    formatter = PostScriptFormatter
    filename = markdown_file.rsplit(".md", 1)[0]
    destination = os.path.join(os.getcwd(), filename)

    do_typeset(markdown_file, formatter, dummy_settings, destination)
    subprocess.check_call(["ps2pdf", filename + ".ps", filename + ".pdf"])
