import pkg_resources
from jinja2 import Template
from typing import List, Union, Set
from .formatter import Formatter, FormatTag, Format as F
from ..domain import Settings


def get_file(name):
    return pkg_resources.resource_string(__name__, name).decode("UTF-8")


template = Template(get_file("postscript_template.ps"))

fonts = "\n".join([
    get_file("iosevka-plus-regular.t42"),
    get_file("iosevka-plus-italic.t42"),
    get_file("iosevka-plus-bold.t42"),
    get_file("iosevka-plus-bold-italic.t42"),
])

reverse_glyphs = get_file("reverse_glyphs.ps")

font_styles = {
    (): "fR",
    (F.Bold,): "fB",
    (F.Italic,): "fI",
    (F.Bold, F.Italic): "fO"
}


def reset_color(settings):
    return "%d fg" % (0 if settings.light else 15)


class PostScriptFormatter(Formatter):
    file_extension = "ps"

    @staticmethod
    def format_tags(line: List[Union[FormatTag, str]], settings) -> str:

        # Regular font, open group
        result = "fR ("

        # For color styles, closing the current group and invoking the next
        # color is enough.
        # For bold / italic / bold-italic, they cannot be combined. Instead,
        # they are separate fonts that have to be selected.

        # TODO: Works for now, but closing two tags in a row will make
        # an empty group: ') u fO (...) u fB () u fR ('

        current_font_styles: Set[F] = set([])

        for elem in line:
            if isinstance(elem, str):
                result += sanitize(elem)
            else:
                tag = elem

                if tag.kind in (F.ForegroundColor, F.BackgroundColor):
                    foreground = tag.kind == F.ForegroundColor

                    if tag.open:
                        color = tag.data["color"]
                        if color[0] != "#":
                            color = "#" + color
                        if foreground:
                            result += ") u 16%s sethexcolor (" % color
                        else:
                            result += ") u /gc 16%s def (" % color
                    else:
                        if foreground:
                            result += ") u %s (" % reset_color(settings)
                        else:
                            result += ") u /gc null def ("

                elif tag.kind in (F.Bold, F.Italic):
                    if tag.open:
                        current_font_styles.add(tag.kind)
                    else:
                        current_font_styles.remove(tag.kind)
                    # Close group, render, switch to correct font, open next
                    key = tuple(
                        sorted(current_font_styles, key=lambda f: f.name)
                    )
                    result += ") u %s (" % font_styles[key]

        # function u renders each character as unicode, in a regular grid
        return result + ") u "

    @staticmethod
    def begin_file(settings: Settings) -> str:
        return template.render(
            fonts=fonts,
            reverse_glyphs=reverse_glyphs,
            page_width=settings.page_width,
            page_height=settings.page_height,
        )

    @staticmethod
    def begin_page(settings: Settings) -> str:
        result = ""
        if not settings.light:
            result += "bk "
        return result + "tr"

    @staticmethod
    def format_line(line: str, settings) -> str:
        return "%s %s n" % (reset_color(settings), line)

    @staticmethod
    def end_page(settings: Settings) -> str:
        return "showpage"

    @staticmethod
    def end_file(settings: Settings) -> str:
        return r"%%EOF"


def sanitize(s: str) -> str:
    s = s.replace("\\", "\\\\")
    s = s.replace("(", r"\(")
    s = s.replace(")", r"\)")
    return s
