from mistletoe import block_token, ast_renderer


def parse_file(path):
    with open(path, "r") as f:
        markdown = f.read()
    return parse_markdown(markdown)


def parse_markdown(markdown):
    document = block_token.Document(markdown.splitlines(keepends=True))
    return ast_renderer.get_ast(document)