# from pygments.lexers import get_lexer_by_name  # type: ignore
import re
from typing import List, Union

from ..domain import document as d
from ..formatting import Formatter, FormatTag


def highlight_code_block(
    code_block: d.CodeBlock,
    formatter: Formatter,
    width: int
) -> List[str]:
    lines = code_block.code.splitlines()
    # Keep the whitespace, this is source code!
    words = [re.split(r"(\s+)", line) for line in lines]

    wrapped: List[List[Union[FormatTag, str]]] = []
    current_length = 0

    def rjust_last():
        if wrapped:
            wrapped[-1].append(" " * (width - current_length))

    def new_line():
        nonlocal current_length
        rjust_last()
        wrapped.append([])
        current_length = 0

    for line in words:
        new_line()
        last_line = wrapped[-1]

        for word in line:
            if current_length + len(word) > width:
                new_line()
                last_line = wrapped[-1]

            last_line.append(word)
            current_length += len(word)

    rjust_last()
    formatted_lines = [formatter.format_tags(l) for l in wrapped]
    return ["".join(l) for l in formatted_lines]
