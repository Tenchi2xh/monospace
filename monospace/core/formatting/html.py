import cgi
from typing import List, Union
from .formatter import Formatter, FormatTag, Format as F
from ..domain import Settings

tags = {
    F.Bold: "b",
    F.Italic: "i",
    F.ForegroundColor: "span",
    F.BackgroundColor: "span",
    F.CrossRef: "a",
}

# FIXME: Keep track of BG/FG appearance
# We don't want to close the wrong tag
tag_attributes = {
    F.ForegroundColor: lambda tag: {"style": "color: %s" % tag.data["color"]},
    F.BackgroundColor: lambda tag: {"style": "background-color: %s"
                                             % tag.data["color"]},
    # This makes the links real but they don't work (no anchors set)
    F.CrossRef: lambda tag: {
        "href": (
            "#%s" % tag.data["identifier"]
            if "identifier" in tag.data
            else "XXX"  # This is related to bug in paragraph.py
        )
    },
}

black_list = [F.Code, F.Quoted]


def tag(format_tag):
    kind = format_tag.kind
    tag_name = tags[kind]

    if kind in tag_attributes and format_tag.open:
        attributes = tag_attributes[kind](format_tag)
        formatted = " ".join('%s="%s"' % (k, v) for k, v in attributes.items())
        return "<%s %s>" % (tag_name, formatted)

    return "<%s%s>" % ("/" if not format_tag.open else "", tag_name)


class HtmlFormatter(Formatter):
    file_extension = "html"
    counter = 0  # Bad!

    @staticmethod
    def format_tags(line: List[Union[FormatTag, str]], settings) -> str:
        result = ""
        for elem in line:
            if isinstance(elem, str):
                result += cgi.escape(elem)
            else:
                if elem.kind not in black_list:
                    result += tag(elem)

        return result

    @staticmethod
    def begin_file(settings: Settings) -> str:
        HtmlFormatter.counter = 0
        fg, bg = ("white", "black")
        if settings.light:
            fg, bg = bg, fg
        return "\n".join([
            "<html>",
            "<head>",
            "<style>",
            "    a { color: %s; }" % fg,
            "    body {",
            "        margin: 0;",
            "        background-color: %s;" % bg,
            "    }",
            "    pre {"
            "        font-family: Iosevka, monospace;",
            "        line-height: 1.2;",
            "        color: %s;" % fg,
            "    }",
            "    a { text-decoration: none }",
            "    a:hover { text-decoration: underline }",
            "    .container { overflow: scroll }",
            "    .page { display: table-cell }",
            "</style>",
            "</head>",
            "<body>",
            '<div class="container">',
        ])

    @staticmethod
    def begin_page(settings: Settings) -> str:
        return '<div class="page"><pre>'

    @staticmethod
    def format_line(line: str, settings) -> str:
        return line

    @staticmethod
    def end_page(settings: Settings) -> str:
        result = "</pre></div>"
        HtmlFormatter.counter += 1
        if HtmlFormatter.counter == 2:
            result += "<br/>"
            HtmlFormatter.counter = 0
        return result

    @staticmethod
    def end_file(settings: Settings) -> str:
        return "</div>\n</body>"
