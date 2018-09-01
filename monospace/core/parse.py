import json
import pypandoc  # type: ignore

try:
    pypandoc._ensure_pandoc_path()
except OSError:
    pypandoc.download_pandoc()
    pypandoc._ensure_pandoc_path()


def parse(source_filename) -> dict:
    raw_ast: str = pypandoc.convert_file(
        source_file=source_filename,
        format="markdown",
        to="json"
    )
    return json.loads(raw_ast)
