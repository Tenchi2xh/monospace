import click

from .read import read
from .typeset import typeset


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
