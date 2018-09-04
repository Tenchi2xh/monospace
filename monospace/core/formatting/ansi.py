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


def reset_fg(settings):
    if settings.light:
        return csi([30], "m")
    return csi([39], "m")


def reset_bg(settings):
    if settings.light:
        return csi([107], "m")
    return csi([49], "m")


def fg_sequence(tag, settings):
    return tag_color(tag, fg=True) if tag.open else reset_fg(settings)


def bg_sequence(tag, settings):
    return tag_color(tag, fg=False) if tag.open else reset_bg(settings)


codes = {
    F.Bold: (csi([1], "m"), csi([22], "m")),
    F.Italic: (csi([3], "m"), csi([23], "m")),
    F.ForegroundColor: fg_sequence,
    F.BackgroundColor: bg_sequence,
}


def get_code(tag, settings):
    code = codes.get(tag.kind, ("", ""))
    if callable(code):
        return code(tag, settings)
    return code[not tag.open]


class AnsiFormatter(Formatter):
    file_extension = "ansi"

    @staticmethod
    def format_tags(line: List[Union[FormatTag, str]], settings) -> str:
        result = ""
        for elem in line:
            if isinstance(elem, str):
                result += elem
            else:
                result += get_code(elem, settings)

        return result

    @staticmethod
    def begin_file(settings: Settings) -> str:
        return ""

    @staticmethod
    def begin_page(settings: Settings) -> str:
        return ""

    @staticmethod
    def format_line(line: str, settings) -> str:
        return reset_fg(settings) + reset_bg(settings) + line + csi([0], "m")

    @staticmethod
    def end_page(settings: Settings) -> str:
        return ""

    @staticmethod
    def end_file(settings: Settings) -> str:
        return ""
