from typing import List, Union
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod, abstractproperty

from ..domain import Settings


@dataclass
class FormatTag:
    kind: str
    open: bool = True

    @property
    def close_tag(self):
        return FormatTag(kind=self.kind, open=False)


class Formatter(metaclass=ABCMeta):
    """A suite of static methods for formatting a file in a given format."""

    @classmethod
    def write_file(cls, path: str, pages: List[List[str]], settings: Settings):
        with open("%s.%s" % (path, cls.file_extension), "w") as f:
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
