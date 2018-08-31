from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FormatTag:
    kind: str
    open: bool = True

    @property
    def close_tag(self):
        return FormatTag(kind=self.kind, open=False)


class Formatter(ABC):
    @staticmethod
    @abstractmethod
    def format_tag(tag: FormatTag) -> str:
        pass
