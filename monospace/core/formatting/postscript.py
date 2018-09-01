import pkg_resources
from jinja2 import Template
from typing import List, Union, Set
from .formatter import Formatter, FormatTag
from ..domain import Settings

raw_template = pkg_resources.resource_string(__name__, "template.ps")
prolog_template = Template(raw_template.decode("UTF-8"))

font_styles = {
    (): "fR",
    ("Bold",): "fB",
    ("Italic",): "fI",
    ("Bold", "Italic"): "fO"
}

DARK_MODE = True


class PostScriptFormatter(Formatter):
    file_extension = "ps"

    @staticmethod
    def format_tags(line: List[Union[FormatTag, str]]) -> str:
        # Reset color, regular font, open group
        result = "%d fg fR (" % (15 if DARK_MODE else 0)

        # For color styles, closing the current group and invoking the next
        # color is enough.
        # For bold / italic / bold-italic, they cannot be combined. Instead,
        # they are separate fonts that have to be selected.

        # TODO: Works for now, but closing two tags in a row will make
        # an empty group: ') u fO (...) u fB () u fR ('

        current_font_styles: Set[str] = set([])

        for elem in line:
            if isinstance(elem, str):
                result += sanitize(elem)
            else:
                tag = elem
                if tag.kind in ("Bold", "Italic"):
                    if tag.open:
                        current_font_styles.add(tag.kind)
                    else:
                        current_font_styles.remove(tag.kind)
                    # Close group, render, switch to correct font, open next
                    key = tuple(sorted(current_font_styles))
                    result += ") u %s (" % font_styles[key]

        # function u renders each character as unicode, in a regular grid
        return result + ") u "

    @staticmethod
    def begin_file(settings: Settings) -> str:
        return prolog_template.render(**vars(settings))

    @staticmethod
    def begin_page(settings: Settings) -> str:
        result = ""
        if DARK_MODE:
            result += "bk "
        return result + "tr"

    @staticmethod
    def format_line(line: str) -> str:
        return "%s n" % line

    @staticmethod
    def end_page(settings: Settings) -> str:
        return "showpage"

    @staticmethod
    def end_file(settings: Settings) -> str:
        return r"%%EOF"


def sanitize(s: str) -> str:
    s = s.replace("(", r"\(")
    s = s.replace(")", r"\)")
    return s
