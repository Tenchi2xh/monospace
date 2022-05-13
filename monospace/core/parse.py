import json

import pypandoc  # type: ignore

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
    return json.loads(raw_ast)
