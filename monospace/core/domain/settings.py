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

    @property
    def page_width(self):
        return (
            self.margin_inside
            + self.margin_outside
            + self.side_width
            + self.side_spacing
            + self.main_width
        )
