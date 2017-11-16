from mistletoe import block_token
from mistletoe import ast_renderer


def parse_file(path):
    with open(path, "r") as f:
        lines = f.read().splitlines(keepends=True)
    document = block_token.Document(lines)
    return ast_renderer.get_ast(document)
