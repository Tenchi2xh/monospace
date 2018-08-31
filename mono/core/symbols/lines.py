# flake8: noqa

from enum import Enum

Styles = Enum("Styles", ["empty", "light", "heavy", "double",
                         "soft", "dash2", "dash3", "dash4"])

empty = Styles.empty
light = Styles.light
heavy = Styles.heavy
double = Styles.double
soft = Styles.soft
dash2 = Styles.dash2
dash3 = Styles.dash3
dash4 = Styles.dash4

# Format: (left, top, right, bottom)
lines = {
    (light,  empty,  light,  empty ): "─",    (empty,  light,  empty,  light ): "│",
    (heavy,  empty,  heavy,  empty ): "━",    (empty,  heavy,  empty,  heavy ): "┃",
    (double, empty,  double, empty ): "═",    (empty,  double, empty,  double): "║",
    (dash2,  empty,  dash2,  empty ): "╌",    (empty,  dash2,  empty,  dash2 ): "╎",
    (dash2,  empty,  dash2,  empty ): "╍",    (empty,  dash2,  empty,  dash2 ): "╏",
    (dash3,  empty,  dash3,  empty ): "┄",    (empty,  dash3,  empty,  dash3 ): "┆",
    (dash3,  empty,  dash3,  empty ): "┅",    (empty,  dash3,  empty,  dash3 ): "┇",
    (dash4,  empty,  dash4,  empty ): "┈",    (empty,  dash4,  empty,  dash4 ): "┊",
    (dash4,  empty,  dash4,  empty ): "┉",    (empty,  dash4,  empty,  dash4 ): "┋",

    (light,  empty,  heavy,  empty ): "╼",    (empty,  light,  empty,  heavy ): "╽",
    (heavy,  empty,  light,  empty ): "╾",    (empty,  heavy,  empty,  light ): "╿",

    (light,  empty,  empty,  empty ): "╴",    (heavy,  empty,  empty,  empty ): "╸",
    (empty,  light,  empty,  empty ): "╵",    (empty,  heavy,  empty,  empty ): "╹",
    (empty,  empty,  light,  empty ): "╶",    (empty,  empty,  heavy,  empty ): "╺",
    (empty,  empty,  empty,  light ): "╷",    (empty,  empty,  empty,  heavy ): "╻",

    (empty,  empty,  light,  light ): "┌",    (light,  empty,  empty,  light ): "┐",
    (empty,  empty,  heavy,  heavy ): "┏",    (heavy,  empty,  empty,  heavy ): "┓",
    (empty,  empty,  double, double): "╔",    (double, empty,  empty,  double): "╗",
    (empty,  empty,  soft,   soft  ): "╭",    (soft,   empty,  empty,  soft  ): "╮",
    (empty,  empty,  heavy,  light ): "┍",    (heavy,  empty,  empty,  light ): "┑",
    (empty,  empty,  light,  heavy ): "┎",    (light,  empty,  empty,  heavy ): "┒",
    (empty,  empty,  double, light ): "╒",    (double, empty,  empty,  light ): "╕",
    (empty,  empty,  light,  double): "╓",    (light,  empty,  empty,  double): "╖",

    (empty,  light,  light,  empty ): "└",    (light,  light,  empty,  empty ): "┘",
    (empty,  heavy,  heavy,  empty ): "┗",    (heavy,  heavy,  empty,  empty ): "┛",
    (empty,  double, double, empty ): "╚",    (double, double, empty,  empty ): "╝",
    (empty,  soft,   soft,   empty ): "╰",    (soft,   soft,   empty,  empty ): "╯",
    (empty,  light,  heavy,  empty ): "┕",    (heavy,  light,  empty,  empty ): "┙",
    (empty,  heavy,  light,  empty ): "┖",    (light,  heavy,  empty,  empty ): "┚",
    (empty,  light,  double, empty ): "╘",    (double, light,  empty,  empty ): "╛",
    (empty,  double, light,  empty ): "╙",    (light,  double, empty,  empty ): "╜",

    (empty,  light,  light,  light ): "├",    (light,  light,  empty,  light ): "┤",
    (empty,  heavy,  heavy,  heavy ): "┣",    (heavy,  heavy,  empty,  heavy ): "┫",
    (empty,  double, double, double): "╠",    (double, double, empty,  double): "╣",
    (empty,  light,  double, light ): "╞",    (double, light,  empty,  light ): "╡",
    (empty,  double, light,  double): "╟",    (light,  double, empty,  double): "╢",
    (empty,  light,  heavy,  light ): "┝",    (heavy,  light,  empty,  light ): "┥",
    (empty,  heavy,  light,  light ): "┞",    (light,  heavy,  empty,  light ): "┦",
    (empty,  light,  light,  heavy ): "┟",    (light,  light,  empty,  heavy ): "┧",
    (empty,  heavy,  light,  heavy ): "┠",    (light,  heavy,  empty,  heavy ): "┨",
    (empty,  heavy,  heavy,  light ): "┡",    (heavy,  heavy,  empty,  light ): "┩",
    (empty,  light,  heavy,  heavy ): "┢",    (heavy,  light,  empty,  heavy ): "┪",

    (light,  empty,  light,  light ): "┬",    (light,  light,  light,  empty ): "┴",
    (heavy,  empty,  heavy,  heavy ): "┳",    (heavy,  heavy,  heavy,  empty ): "┻",
    (double, empty,  double, double): "╦",    (double, double, double, empty ): "╩",
    (double, empty,  double, light ): "╤",    (double, light,  double, empty ): "╧",
    (light,  empty,  light,  double): "╥",    (light,  double, light,  empty ): "╨",
    (heavy,  empty,  light,  light ): "┭",    (heavy,  light,  light,  empty ): "┵",
    (light,  empty,  heavy,  light ): "┮",    (light,  light,  heavy,  empty ): "┶",
    (heavy,  empty,  heavy,  light ): "┯",    (heavy,  light,  heavy,  empty ): "┷",
    (light,  empty,  light,  heavy ): "┰",    (light,  heavy,  light,  empty ): "┸",
    (heavy,  empty,  light,  heavy ): "┱",    (heavy,  heavy,  light,  empty ): "┹",
    (light,  empty,  heavy,  heavy ): "┲",    (light,  heavy,  heavy,  empty ): "┺",

    (light,  light,  light,  light ): "┼",    (double, double, double, double): "╬",
    (double, light,  double, light ): "╪",    (light,  double, light,  double): "╫",

    (heavy,  light,  light,  light ): "┽",    (light,  heavy,  heavy,  light ): "╄",
    (light,  light,  heavy,  light ): "┾",    (heavy,  light,  light,  heavy ): "╅",
    (heavy,  light,  heavy,  light ): "┿",    (light,  light,  heavy,  heavy ): "╆",
    (light,  heavy,  light,  light ): "╀",    (heavy,  heavy,  heavy,  light ): "╇",
    (light,  light,  light,  heavy ): "╁",    (heavy,  light,  heavy,  heavy ): "╈",
    (light,  heavy,  light,  heavy ): "╂",    (heavy,  heavy,  light,  heavy ): "╉",
    (heavy,  heavy,  light,  light ): "╃",    (light,  heavy,  heavy,  heavy ): "╊",
    (heavy,  heavy,  heavy,  heavy ): "╋",

    (empty,  empty,  empty,  empty ): " ",
}
