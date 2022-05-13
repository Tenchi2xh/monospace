import re
from copy import copy
from pathlib import Path


# https://stackoverflow.com/a/6300649
def intersperse(sequence, value):
    result = [copy(value) for _ in range(2 * len(sequence) - 1)]
    result[::2] = sequence
    return result


def concatenate_markdown_directory(directory):
    all_markdown = sorted(Path(directory).rglob("*.md"))

    content = ""
    for path in all_markdown:
        rel_path = path.relative_to(directory).parent
        with open(path, "r") as f:
            markdown = f.read()
            # FIXME: better fix for relative links?
            markdown = re.sub(
                r'!\[(.*)\]\((.*)\)',
                f"![\\1]({rel_path}/\\2)",
                markdown
            )
            content += markdown
            content += "\n\n"
    content = re.sub(r"\n\n\n+", "\n\n", content)

    return content
