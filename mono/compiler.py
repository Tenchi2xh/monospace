from .context import Context
from .book import Book
from .util.lang import auto_repr
from .formatting.terminal import convert


@auto_repr
class FormatTag(object):
    def __init__(self, cursor, type, start, target=None):
        self.cursor = cursor
        self.type = type
        self.start = start
        self.target = target

    def flip(self):
        return FormatTag(self.cursor, self.type, not self.start, self.target)


def compile(context):
    if isinstance(context, Book):
        context = Context(context)

    elements = []

    for child in context.book.ast["children"]:
        t = child["type"]
        if t == "Heading":
            level = child["level"] - 1
            for i in range(level + 1, len(context.chapter)):
                context.chapter[i] = 0
            context.chapter[level] += 1

            display = context.chapter[0:context.chapter.index(0)]
            chapter = "%d." % display[0] if len(display) == 1 else ".".join(str(n) for n in display)

            chapter_node = {
                "type": "RawText",
                "content": chapter + " "
            }
            elements.append(format_text([chapter_node] + child["children"]))

        elif t == "Paragraph":
            elements.append(format_text(child["children"]))

        else:
            print("MISSING: " + t)

    return elements


def format_text(nodes, cursor=0):
    text = ""
    formatting = []

    for node in nodes:
        content = node["content"] if "content" in node else ""
        node_type = node["type"]
        not_raw = node_type != "RawText"
        target = node["target"] if "target" in node else None

        if not_raw:
            formatting.append(FormatTag(cursor=cursor, type=node_type, start=True, target=target))

        if content:
            text += content
        else:
            nested_text, nested_formatting, cursor = format_text(node["children"], cursor=cursor)
            text += nested_text
            formatting.extend(nested_formatting)

        if not_raw:
            formatting.append(FormatTag(cursor=cursor, type=node_type, start=False, target=target))

        cursor += len(content)

    return (text, formatting, cursor)
