import json

import pypandoc  # type: ignore
from leet.logging import log

try:
    pypandoc._ensure_pandoc_path()
except OSError:
    pypandoc.download_pandoc()
    pypandoc._ensure_pandoc_path()


def parse(markdown_content) -> dict:
    raw_ast: str = pypandoc.convert_text(
        markdown_content,
        format="markdown",
        to="json"
    )
    log.debug("Parsing markdown AST using Pandoc (%d chars)..." % len(markdown_content))
    return json.loads(raw_ast)
