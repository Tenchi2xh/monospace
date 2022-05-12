from typing import List
from dataclasses import dataclass


@dataclass
class Settings:
    main_width: int
    page_height: int
    side_width: int
    side_spacing: int
    tab_size: int

    margin_top: int
    margin_inside: int
    margin_outside: int
    margin_bottom: int

    break_before: List[str]

    working_dir: str
    light: bool
    github_anchors: bool

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
        return Settings(
            main_width=get(meta, "dimensions.body-width", 70),
            page_height=get(meta, "dimensions.page-height", 60),
            side_width=get(meta, "dimensions.notes-width", 30),
            side_spacing=get(meta, "dimensions.separation", 4),
            tab_size=get(meta, "dimensions.indentations", 4),
            break_before=get(meta, "break-before", ["Chapter", "SubChapter"]),
            margin_top=get(meta, "dimensions.margins.top", 5),
            margin_inside=get(meta, "dimensions.margins.inside", 10),
            margin_outside=get(meta, "dimensions.margins.outside", 5),
            margin_bottom=get(meta, "dimensions.margins.bottom", 5),
            working_dir=working_dir,
            light=get(meta, "light-theme", False),
            github_anchors=get(meta, "github-anchors", False)
        )


def get(dictionary, key, default):
    keys = key.split(".")
    current = dictionary
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
