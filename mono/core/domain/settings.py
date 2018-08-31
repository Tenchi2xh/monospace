from dataclasses import dataclass


@dataclass
class Settings:
    page_width: int
    page_height: int
    margin_top: int
    margin_inside: int
    margin_outside: int
    margin_bottom: int
    margin_spacing: int
    tab_size: int
