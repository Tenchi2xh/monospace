import pkg_resources
from jinja2 import Template
from typing import List, Union
from .formatter import Formatter, FormatTag
from ..domain import Settings

raw_template = pkg_resources.resource_string(__name__, "template.ps")
prolog_template = Template(raw_template.decode("UTF-8"))


class PostScriptFormatter(Formatter):
    file_extension = "ps"

    @staticmethod
    def format_tags(line: List[Union[FormatTag, str]]) -> str:
        result = "("
        for elem in line:
            if isinstance(elem, str):
                result += sanitize(elem)

        return result + ") u "

    @staticmethod
    def begin_file(settings: Settings) -> str:
        return prolog_template.render(**vars(settings))

    @staticmethod
    def begin_page(settings: Settings) -> str:
        return "tr"

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
