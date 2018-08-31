from dataclasses import dataclass


@dataclass
class Settings:
    page_width: int
    page_height: int
    margin_top: int
    margin_inside: int
    margin_outside: int
    margin_bottom: int
    side_spacing: int
    tab_size: int

    @property
    def editable_width(self):
        return (
            self.page_width
            - self.margin_inside
            - self.margin_outside
        )

    @property
    def main_width(self):
        return int(0.75 * (self.editable_width - self.side_spacing))

    @property
    def side_width(self):
        return self.editable_width - self.side_spacing - self.main_width
