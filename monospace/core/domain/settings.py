from dataclasses import dataclass
from typing import Dict, Generic, List, TypeVar

from ...util import flatten_dict

T = TypeVar("T")


@dataclass
class Setting(Generic[T]):
    key: str
    help: str
    default: T


schema = {
    "Page dimensions": {
        "main_width": Setting[int](
            key="dimensions.body-width",
            help="Width of the main content (text body)",
            default=70
        ),
        "page_height": Setting[int](
            key="dimensions.page-height",
            help="Height of the page from top to bottom including margins",
            default=60,
        ),
        "side_width": Setting[int](
            key="dimensions.notes-width",
            help="Width of the side content (footnotes, subtitles, captions)",
            default=30,
        ),
    },
    "Margins": {
        "margin_top": Setting[int](
            key="dimensions.margins.top",
            help="Margin at the top of the page, before the text body",
            default=5,
        ),
        "margin_inside": Setting[int](
            key="dimensions.margins.inside",
            help="Margin on the inside of the page (right on a left page, left on a right page)",
            default=10,
        ),
        "margin_outside": Setting[int](
            key="dimensions.margins.outside",
            help="Margin on the outside of the page (left on a left page, right on a right page)",
            default=5,
        ),
        "margin_bottom": Setting[int](
            key="dimensions.margins.bottom",
            help="Margin at the bottom of the page, after the text body",
            default=5,
        ),
    },
    "Spacings": {
        "side_spacing": Setting[int](
            key="dimensions.separation",
            help="Gap between the side content and the main content",
            default=4,
        ),
        "tab_size": Setting[int](
            key="dimensions.indentations",
            help="Width of indentations (for lists, etc.)",
            default=4,
        ),
    },
    "Document settings": {
        "light": Setting[bool](
            key="light-theme",
            help="Output using a black-on-white color scheme",
            default=False,
        ),
        "break_before": Setting[List[str]](
            key="break-before",
            help="Element types before which a page break should happen",
            default=["Chapter", "SubChapter"],
        ),
        "github_anchors": Setting[bool](
            key="github-anchors",
            help="Enable GitHub style anchor references in internal links",
            default=False,
        ),
        "draw_borders": Setting[bool](
            key="draw-borders",
            help="Draw border around the pages (mostly for debugging)",
            default=False,
        ),
        "dictionary": Setting[List[str]](
            key="dictionary",
            help="List of words to ignore during spell-check",
            default=[],
        ),
    },
}

flat_schema: Dict[str, Setting] = flatten_dict(schema)


@dataclass
class Settings:
    # Page dimensions
    main_width: int
    page_height: int
    side_width: int
    # Margins
    margin_top: int
    margin_inside: int
    margin_outside: int
    margin_bottom: int
    # Spacings
    side_spacing: int
    tab_size: int
    # Document settings
    light: bool
    break_before: List[str]
    github_anchors: bool
    draw_borders: bool
    dictionary: List[str]
    # Internal use
    working_dir: str

    @property
    def page_width(self):
        return (
            self.margin_inside
            + self.margin_outside
            + self.side_width
            + self.side_spacing
            + self.main_width
        )

    @staticmethod
    def from_meta(meta, working_dir):
        kwargs = {n: get(meta, s.key, s.default) for n, s in flat_schema.items()}
        settings = Settings(
            working_dir=working_dir,
            **kwargs,
        )
        settings.dictionary = [w.lower() for w in settings.dictionary]
        return settings


def get(dictionary, key, default):
    keys = key.split(".")
    current = dictionary
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
