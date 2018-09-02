import click

from .read import read
from .typeset import typeset
from .pdf import pdf


@click.group()
def monospace():
    """
    \b
    ┌─────┬───┬───┬───┬───┬───┬───┬───┬───┐
    │ ╷ ╷ │ · │ ╷ │ · ├   ┤ · │ · │   ┤   ╡
    └─┴─┴─┴───┴─┴─┴───┴───┤ ┌─┴─┴─┴───┴───┘
                          └─┘
         A fixed-width book typesetter
    """
    pass


monospace.add_command(read)
monospace.add_command(typeset)
monospace.add_command(pdf)
