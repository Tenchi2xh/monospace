import io
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Union, Any, Dict
from abc import ABCMeta, abstractmethod, abstractproperty

from ..domain import Settings

Format = Enum("Format", [
    "Bold", "Italic",
    "Code", "Quoted", "CrossRef",
    # Warning: nesting colors of the same type will not be supported
    "ForegroundColor", "BackgroundColor"
])


@dataclass
class FormatTag:
    kind: Format
    open: bool = True
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def close_tag(self):
        return FormatTag(kind=self.kind, open=False)


class Formatter(metaclass=ABCMeta):
    """A suite of static methods for formatting a file in a given format."""

    @classmethod
    def write_file(cls, path: str, pages: List[List[str]], settings: Settings):
        def do_write(f):
            def w(s):
                f.write(s)
                f.write("\n")

            w(cls.begin_file(settings))
            for page in pages:
                w(cls.begin_page(settings))
                for line in page:
                    w(cls.format_line(line))
                w(cls.end_page(settings))
            w(cls.end_file(settings))

        if isinstance(path, io.IOBase):
            do_write(path)
        else:
            with open("%s.%s" % (path, cls.file_extension), "w") as f:
                do_write(f)

    @staticmethod
    @abstractmethod
    def format_tags(line: List[Union[FormatTag, str]]) -> str:
        """Returns the formatting necessary for given tags.

        This is used in `paragraph.align`, but must also
        be used for any inserted text in `Renderer` or in `layout`.
        """

    @abstractproperty
    def file_extension(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def begin_file(settings: Settings) -> str:
        """Returns the beginning of a file necessary for this format."""

    @staticmethod
    @abstractmethod
    def begin_page(settings: Settings) -> str:
        """Returns the formatting necessary for beginning a page."""

    @staticmethod
    @abstractmethod
    def format_line(line: str) -> str:
        """Formats a line in this format.

        The line must have been formatted using `format_tag` calls.
        """

    @staticmethod
    @abstractmethod
    def end_page(settings: Settings) -> str:
        """Returns the formatting necessary for ending a page."""

    @staticmethod
    @abstractmethod
    def end_file(settings: Settings) -> str:
        """Returns the end of a file necessary for this format."""
