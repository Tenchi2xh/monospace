from typing import List, Union
from .formatter import Formatter, FormatTag


def csi(params, end):
    return "\033[%s%s" % (";".join(str(p) for p in params), end)


codes = {
    "Bold": (csi([1], "m"), csi([22], "m")),
    "Italic": (csi([3], "m"), csi([23], "m")),
}


class AnsiFormatter(Formatter):
    @staticmethod
    def format_tags(line: List[Union[FormatTag, str]]) -> str:
        result = ""
        for elem in line:
            if isinstance(elem, str):
                result += elem
            else:
                tag = elem
                result += codes.get(tag.kind, ("", ""))[int(not tag.open)]

        return result
