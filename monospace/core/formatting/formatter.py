from abc import ABCMeta, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from enum import Enum
from io import TextIOWrapper as IOStream
from typing import Any, Dict, List, Union

from leet.logging import log

from ..domain import Settings

Format = Enum("Format", [
    "Bold", "Italic",
    "Code", "Quoted", "CrossRef", "Anchor",
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
    def write_file(cls, output: Union[str, IOStream], pages: List[List[str]], settings: Settings):
        output_name = str(output.name) if isinstance(output, IOStream) else output
        log.debug(f"Writing final book to '{output_name}' using renderer '{cls.__name__}'...")

        def do_write(f):
            def w(s):
                f.write(s)
                f.write("\n")

            w(cls.begin_file(settings))
            for page in pages:
                w(cls.begin_page(settings))
                for line in page:
                    w(cls.format_line(line, settings))
                w(cls.end_page(settings))
            w(cls.end_file(settings))

        if isinstance(output, IOStream):
            do_write(output)
        else:
            with open("%s.%s" % (output, cls.file_extension), "w") as f:
                do_write(f)

    @staticmethod
    @abstractmethod
    def format_tags(line: List[Union[FormatTag, str]], settings) -> str:
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
    def format_line(line: str, settings: Settings) -> str:
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
