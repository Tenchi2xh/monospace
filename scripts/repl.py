#!/usr/bin/env python3

import importlib
import sys

from better_exceptions import ExceptionFormatter
from ptpython.entry_points.run_ptpython import run
from ptpython.repl import embed


def rgb(h):
    components = [int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16)]
    return ";".join(map(str, components))


theme = {
    'comment': lambda s: '\x1b[38;2;{}m{}\x1b[m'.format(rgb("6C6C6C"), s),
    'keyword': lambda s: '\x1b[38;2;{}m{}\x1b[m'.format(rgb("7AD1F5"), s),
    'builtin': lambda s: '\x1b[38;2;{}m{}\x1b[m'.format(rgb("B5D142"), s),
    'literal': lambda s: '\x1b[38;2;{}m{}\x1b[m'.format(rgb("C1BF81"), s),
    'inspect': lambda s: '\x1b[38;2;{}m{}\x1b[m'.format(rgb("A98CF8"), s),
}


def format_exception(exc, value, tb):
    formatter = ExceptionFormatter(colored=True, theme=theme, max_length=128,
                                   pipe_char="│", cap_char="└")
    return formatter.format_exception(exc, value, tb)


def _handle_exception(cls, cli, e):
    output = cli.output

    t, v, tb = sys.exc_info()
    tb = tb.tb_next.tb_next

    formatted = format_exception(t, v, tb)
    output.stdout.write(formatted)
    output.stdout.flush()


if __name__ == "__main__":
    setattr(embed.__globals__["PythonRepl"], "_handle_exception", _handle_exception)
    run.__globals__["embed"] = embed

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            module = importlib.import_module(arg)
            try:
                to_import = module.__all__
            except AttributeError:
                to_import = [name for name in module.__dict__ if not name.startswith('_')]
            globals().update({name: module.__dict__[name] for name in to_import})
        sys.argv = sys.argv[:1]

    run()
