from typing import List, Union
from .formatter import Formatter, FormatTag, Format as F

tags = {
    F.Bold: "b",
    F.Italic: "i",
}


def tag(format_tag):
    return "<%s%s>" % (
        "/" if not format_tag.open else "",
        tags[format_tag.kind]
    )


class HtmlFormatter(Formatter):
    @staticmethod
    def format_tags(line: List[Union[FormatTag, str]]) -> str:
        result = ""
        for elem in line:
            if isinstance(elem, str):
                result += elem
            else:
                result += tag(elem)

        return result
