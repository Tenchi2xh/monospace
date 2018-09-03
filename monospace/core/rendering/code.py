import re
from typing import List, Union
from pygments.lexers import get_lexer_by_name  # type: ignore
from pygments.styles import get_style_by_name  # type: ignore
from pygments.token import Token  # type: ignore
from pygments.util import ClassNotFound  # type: ignore

from ..domain import document as d
from ..formatting import Formatter, FormatTag, Format as F


def highlight_code_block(
    code_block: d.CodeBlock,
    formatter: Formatter,
    width: int
) -> List[str]:
    try:
        lexer = get_lexer_by_name(code_block.language)
    except ClassNotFound:
        lexer = None

    # Pygments styles are in this format:
    # ['fg hex', bold, nobold, italic, noitalic, ul, noul, 'bg hex',
    #  border, roman, sans, mono]
    # (https://github.com/nex3/pygments/blob/master/pygments/style.py#L49)
    # hex values have no leading '#'
    style = get_style_by_name("monokai")  # TODO: Make this a setting + meta

    words: List[List[Union[FormatTag, str]]] = [[]]

    if lexer:
        for e in list(lexer.get_tokens(code_block.code)):
            # Map pygments styles for each token to a list of FormatTag
            style_map = {}
            for token_type, values in style._styles.items():
                tags = []
                if values[0]:
                    tags.append(FormatTag(
                        kind=F.ForegroundColor,
                        data={"color": "#" + values[0]}
                    ))
                style_map[token_type] = tags

        tokens = lexer.get_tokens(code_block.code)
        last_line = words[-1]
        for token, word in tokens:
            if (token, word) == (Token.Text, "\n"):
                words.append([])
                last_line = words[-1]
                continue

            tags = style_map[token]
            last_line.extend(tags)
            last_line.append(word)
            last_line.extend([tag.close_tag for tag in tags])

        # Remove trailing empty line
        if not last_line:
            words.pop()
    else:
        lines = code_block.code.splitlines()
        # Keep the whitespace, this is source code!
        words = [re.split(r"(\s+)", line) for line in lines]  # type: ignore

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
            if isinstance(word, FormatTag):
                last_line.append(word)
                continue
            if current_length + len(word) > width:
                new_line()
                last_line = wrapped[-1]

            last_line.append(word)
            current_length += len(word)

    rjust_last()
    formatted_lines = [formatter.format_tags(l) for l in wrapped]
    return ["".join(l) for l in formatted_lines]
