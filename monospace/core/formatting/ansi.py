from typing import List, Union
from ..domain import Settings
from .formatter import Formatter, FormatTag, Format as F


def csi(params, end):
    return "\033[%s%s" % (";".join(str(p) for p in params), end)


def rgb(hexa):
    if hexa[0] == "#":
        hexa = hexa[1:]
    return int(hexa[:2], 16), int(hexa[2:4], 16), int(hexa[4:6], 16)


def tag_color(tag, fg):
    return csi([38 if fg else 48, 2, *rgb(tag.data["color"])], "m")


codes = {
    F.Bold: (csi([1], "m"), csi([22], "m")),
    F.Italic: (csi([3], "m"), csi([23], "m")),
    F.ForegroundColor: lambda tag: (tag_color(tag, fg=True)
                                    if tag.open else csi([39], "m")),
    F.BackgroundColor: lambda tag: (tag_color(tag, fg=False)
                                    if tag.open else csi([49], "m"))
}


def get_code(tag):
    code = codes.get(tag.kind, ("", ""))
    if callable(code):
        return code(tag)
    return code[not tag.open]


class AnsiFormatter(Formatter):
    file_extension = "ansi"

    @staticmethod
    def format_tags(line: List[Union[FormatTag, str]]) -> str:
        result = ""
        for elem in line:
            if isinstance(elem, str):
                result += elem
            else:
                result += get_code(elem)

        return result

    @staticmethod
    def begin_file(settings: Settings) -> str:
        return ""

    @staticmethod
    def begin_page(settings: Settings) -> str:
        return ""

    @staticmethod
    def format_line(line: str) -> str:
        return line

    @staticmethod
    def end_page(settings: Settings) -> str:
        return ""

    @staticmethod
    def end_file(settings: Settings) -> str:
        return ""
