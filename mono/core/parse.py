import json
import pypandoc

try:
    pypandoc._ensure_pandoc_path()
except OSError:
    pypandoc.download_pandoc()
    pypandoc._ensure_pandoc_path()


def parse(source_filename):
    raw_ast = pypandoc.convert_file(source_filename, "json")
    return json.loads(raw_ast)
