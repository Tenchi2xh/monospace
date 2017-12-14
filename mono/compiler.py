from .context import Context
from .book import Book
from .util.lang import auto_repr
from .formatting.terminal import convert


@auto_repr
class FormatTag(object):
    def __init__(self, cursor, type, start):
        self.cursor = cursor
        self.type = type
        self.start = start


def compile(context):
    if isinstance(context, Book):
        context = Context(context)

    elements = []

    for child in context.book.ast["children"]:
        t = child["type"]
        if t == "Heading":
            pass
        elif t == "Paragraph":
            pass

    text, formatting, _ = format_text(context.book.ast["children"][2]["children"])
    result = ""
    j = 0
    for i, char in enumerate(text):
        while j < len(formatting) and formatting[j].cursor == i:
            result += convert(formatting[j])
            j += 1
        result += char

    print(result)

    return elements


def format_text(nodes, cursor=0):
    text = ""
    formatting = []

    for node in nodes:
        content = node["content"] if "content" in node else ""
        node_type = node["type"]
        not_raw = node_type != "RawText"

        if not_raw:
            formatting.append(FormatTag(cursor=cursor, type=node_type, start=True))

        if content:
            text += content
        else:
            nested_text, nested_formatting, cursor = format_text(node["children"], cursor=cursor)
            text += nested_text
            formatting.extend(nested_formatting)

        if not_raw:
            formatting.append(FormatTag(cursor=cursor, type=node_type, start=False))

        cursor += len(content)

    return (text, formatting, cursor)
