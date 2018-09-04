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

    source_file: str
    light: bool

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
    def from_meta(meta, source_file):
        return Settings(
            main_width=get(meta, "dimensions.body-width", 70),
            page_height=get(meta, "dimensions.page-height", 20),
            side_width=get(meta, "dimensions.notes-width", 60),
            side_spacing=get(meta, "dimensions.separation", 4),
            tab_size=get(meta, "dimensions.indentations", 4),
            margin_top=get(meta, "dimensions.margins.top", 5),
            margin_inside=get(meta, "dimensions.margins.inside", 10),
            margin_outside=get(meta, "dimensions.margins.outside", 5),
            margin_bottom=get(meta, "dimensions.margins.bottom", 5),
            source_file=source_file,
            light=get(meta, "light-theme", False)
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
