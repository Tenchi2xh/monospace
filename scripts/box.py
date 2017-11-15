#!/usr/bin/env python3

empty = "empty"
light, heavy, double, soft = "light", "heavy", "double", "soft"
dash2, dash3, dash4 = "double dash", "triple dash", "quadruple dash"

lines = {
#    left    top     right   bottom
    (light,  empty,  light,  empty ): "─",
    (heavy,  empty,  heavy,  empty ): "━",
    (double, empty,  double, empty ): "═",
    (empty,  empty,  empty,  empty ): " ",
    (dash2,  empty,  dash2,  empty ): "╌",
    (dash2,  empty,  dash2,  empty ): "╍",
    (dash3,  empty,  dash3,  empty ): "┄",
    (dash3,  empty,  dash3,  empty ): "┅",
    (dash4,  empty,  dash4,  empty ): "┈",
    (dash4,  empty,  dash4,  empty ): "┉",

    (empty,  light,  empty,  light ): "│",
    (empty,  heavy,  empty,  heavy ): "┃",
    (empty,  double, empty,  double): "║",
    (empty,  empty,  empty,  empty ): " ",
    (empty,  dash2,  empty,  dash2 ): "╎",
    (empty,  dash2,  empty,  dash2 ): "╏",
    (empty,  dash3,  empty,  dash3 ): "┆",
    (empty,  dash3,  empty,  dash3 ): "┇",
    (empty,  dash4,  empty,  dash4 ): "┊",
    (empty,  dash4,  empty,  dash4 ): "┋",

    (empty,  empty,  light,  light ): "┌",
    (empty,  empty,  heavy,  heavy ): "┏",
    (empty,  empty,  double, double): "╔",
    (empty,  empty,  soft,   soft  ): "╭",
    (empty,  empty,  heavy,  light ): "┍",
    (empty,  empty,  light,  heavy ): "┎",
    (empty,  empty,  double, light ): "╒",
    (empty,  empty,  light,  double): "╓",

    (light,  empty,  empty,  light ): "┐",
    (heavy,  empty,  empty,  heavy ): "┓",
    (double, empty,  empty,  double): "╗",
    (soft,   empty,  empty,  soft  ): "╮",
    (heavy,  empty,  empty,  light ): "┑",
    (light,  empty,  empty,  heavy ): "┒",
    (double, empty,  empty,  light ): "╕",
    (light,  empty,  empty,  double): "╖",

    (empty,  light,  light,  empty ): "└",
    (empty,  heavy,  heavy,  empty ): "┗",
    (empty,  double, double, empty ): "╚",
    (empty,  soft,   soft,   empty ): "╰",
    (empty,  light,  heavy,  empty ): "┕",
    (empty,  heavy,  light,  empty ): "┖",
    (empty,  light,  double, empty ): "╘",
    (empty,  double, light,  empty ): "╙",

    (light,  light,  empty,  empty ): "┘",
    (heavy,  heavy,  empty,  empty ): "┛",
    (double, double, empty,  empty ): "╝",
    (soft,   soft,   empty,  empty ): "╯",
    (heavy,  light,  empty,  empty ): "┙",
    (light,  heavy,  empty,  empty ): "┚",
    (double, light,  empty,  empty ): "╛",
    (light,  double, empty,  empty ): "╜",

    (light,  empty,  empty,  empty ): "╴",
    (empty,  light,  empty,  empty ): "╵",
    (empty,  empty,  light,  empty ): "╶",
    (empty,  empty,  empty,  light ): "╷",
    (heavy,  empty,  empty,  empty ): "╸",
    (empty,  heavy,  empty,  empty ): "╹",
    (empty,  empty,  heavy,  empty ): "╺",
    (empty,  empty,  empty,  heavy ): "╻",

    (light,  light,  light,  light ): "┼",
    (heavy,  heavy,  heavy,  heavy ): "╋",
    (double, double, double, double): "╬",
    (double, light,  double, light ): "╪",
    (light,  double, light,  double): "╫",
    (heavy,  light,  light,  light ): "┽",
    (light,  light,  heavy,  light ): "┾",
    (heavy,  light,  heavy,  light ): "┿",
    (light,  heavy,  light,  light ): "╀",
    (light,  light,  light,  heavy ): "╁",
    (light,  heavy,  light,  heavy ): "╂",
    (heavy,  heavy,  light,  light ): "╃",
    (light,  heavy,  heavy,  light ): "╄",
    (heavy,  light,  light,  heavy ): "╅",
    (light,  light,  heavy,  heavy ): "╆",
    (heavy,  heavy,  heavy,  light ): "╇",
    (heavy,  light,  heavy,  heavy ): "╈",
    (heavy,  heavy,  light,  heavy ): "╉",
    (light,  heavy,  heavy,  heavy ): "╊",

    (empty,  light,  light,  light ): "├",
    (empty,  heavy,  heavy,  heavy ): "┣",
    (empty,  double, double, double): "╠",
    (empty,  light,  double, light ): "╞",
    (empty,  double, light,  double): "╟",
    (empty,  light,  heavy,  light ): "┝",
    (empty,  heavy,  light,  light ): "┞",
    (empty,  light,  light,  heavy ): "┟",
    (empty,  heavy,  light,  heavy ): "┠",
    (empty,  heavy,  heavy,  light ): "┡",
    (empty,  light,  heavy,  heavy ): "┢",

    (light,  light,  empty,  light ): "┤",
    (heavy,  heavy,  empty,  heavy ): "┫",
    (double, double, empty,  double): "╣",
    (double, light,  empty,  light ): "╡",
    (light,  double, empty,  double): "╢",
    (heavy,  light,  empty,  light ): "┥",
    (light,  heavy,  empty,  light ): "┦",
    (light,  light,  empty,  heavy ): "┧",
    (light,  heavy,  empty,  heavy ): "┨",
    (heavy,  heavy,  empty,  light ): "┩",
    (heavy,  light,  empty,  heavy ): "┪",

    (light,  empty,  light,  light ): "┬",
    (heavy,  empty,  heavy,  heavy ): "┳",
    (double, empty,  double, double): "╦",
    (double, empty,  double, light ): "╤",
    (light,  empty,  light,  double): "╥",
    (heavy,  empty,  light,  light ): "┭",
    (light,  empty,  heavy,  light ): "┮",
    (heavy,  empty,  heavy,  light ): "┯",
    (light,  empty,  light,  heavy ): "┰",
    (heavy,  empty,  light,  heavy ): "┱",
    (light,  empty,  heavy,  heavy ): "┲",

    (light,  light,  light,  empty ): "┴",
    (heavy,  heavy,  heavy,  empty ): "┻",
    (double, double, double, empty ): "╩",
    (double, light,  double, empty ): "╧",
    (light,  double, light,  empty ): "╨",
    (heavy,  light,  light,  empty ): "┵",
    (light,  light,  heavy,  empty ): "┶",
    (heavy,  light,  heavy,  empty ): "┷",
    (light,  heavy,  light,  empty ): "┸",
    (heavy,  heavy,  light,  empty ): "┹",
    (light,  heavy,  heavy,  empty ): "┺",

    (light,  empty,  heavy,  empty ): "╼",
    (empty,  light,  empty,  heavy ): "╽",
    (heavy,  empty,  light,  empty ): "╾",
    (empty,  heavy,  empty,  light ): "╿",
}

diagonals = "╱╲╳"


class Cell(object):
    def __init__(self, left=None, top=None, right=None, bottom=None):
        self.left, self.top, self.right, self.bottom = left, top, right, bottom

    @property
    def all(self):
        return [self.left, self.top, self.right, self.bottom]


class EmptyMetaCell(object):
    def __init__(self):
        self.styles = Cell(empty, empty, empty, empty)


class MetaCell(object):
    def __init__(self, left, top, right, bottom):
        self.styles = Cell(left=left, top=top, right=right, bottom=bottom)
        self.neighbours = Cell(EmptyMetaCell(), EmptyMetaCell(), EmptyMetaCell(), EmptyMetaCell())

    @staticmethod
    def all_sides(weight):
        return MetaCell(weight, weight, weight, weight)

    @staticmethod
    def make(format_string):
        if len(format_string) == 1:
            return {
                "L": MetaCell.all_sides(light),
                "H": MetaCell.all_sides(heavy),
                "D": MetaCell.all_sides(double)
            }[format_string]

        elif len(format_string) == 4:
            left, top, right, bottom = map(lambda l: MetaCell.long_format[l], format_string)
            return MetaCell(left=left, top=top, right=right, bottom=bottom)

    def __repr__(self):
        def long_format(meta_cell):
            return [MetaCell.reverse_long_format[s] for s in meta_cell.styles.all]

        styles = long_format(self)
        neighbours = "(%s, %s, %s, %s)" % (long_format(self.neighbours.left),
                                           long_format(self.neighbours.top),
                                           long_format(self.neighbours.right),
                                           long_format(self.neighbours.bottom))

        return "Cell(Styles: %s, Neighbours: %s)" % (styles, neighbours)


MetaCell.long_format = {"l": light, "h": heavy, "d": double, "e": empty}
MetaCell.reverse_long_format = {v: k for k, v in MetaCell.long_format.items()}
MetaCell.reverse_long_format.update({empty: "."})


def print_cell_grid(cells):
    for cell_line in cells:
        result_line = ["" for _ in range(5)]
        for cell in cell_line:
            rf = MetaCell.reverse_long_format

            left0, top0, right0, bottom0 = (rf[cell.styles.left],
                                            rf[cell.styles.top],
                                            rf[cell.styles.right],
                                            rf[cell.styles.bottom])

            left1, top1, right1, bottom1 = (rf[cell.neighbours.left.styles.right],
                                            rf[cell.neighbours.top.styles.bottom],
                                            rf[cell.neighbours.right.styles.left],
                                            rf[cell.neighbours.bottom.styles.top])

            result_line[0] += "    %s       " % top1
            result_line[1] += "    %s       " % top0
            result_line[2] += "%s %s   %s %s   " % (left1, left0, right0, right1)
            result_line[3] += "    %s       " % bottom0
            result_line[4] += "    %s       " % bottom1

        for l in result_line:
            print(l)
        print()


def make_cell_grid(formats):
    height = len(formats)
    width = len(formats[0])
    assert all(len(line) == width for line in formats)

    cells = [[MetaCell.make(format_string) for format_string in line] for line in formats]

    for y in range(height):
        for x in range(width):
            if y > 0:
                cells[y][x].neighbours.top = cells[y - 1][x]
            if y < height - 1:
                cells[y][x].neighbours.bottom = cells[y + 1][x]
            if x > 0:
                cells[y][x].neighbours.left = cells[y][x - 1]
            if x < width - 1:
                cells[y][x].neighbours.right = cells[y][x + 1]

    return cells


def draw_box(formats, contents):
    cells = make_cell_grid(formats)
    print_cell_grid(cells)

    height = len(cells)
    width = len(cells[0])

    for y, line in enumerate(cells):
        top = ""
        middle = ""
        bottom = ""

        for x, cell in enumerate(line):
            s = cell.styles
            l = cell.neighbours.left.styles
            t = cell.neighbours.top.styles
            r = cell.neighbours.right.styles
            b = cell.neighbours.bottom.styles

            # Strategy: draw left and top sides of current cell,
            # unless last column or last row

            top    += lines[(l.top, t.left, s.top, s.left)]
            middle += lines[(empty, s.left, empty, s.left)]

            top    += 3 * lines[(s.top, empty, s.top, empty)]  # Multiply by content width
            middle += 3 * " "  # Replace with content

            if x == width - 1:
                top    += lines[(s.top, t.right, empty, s.right)]
                middle += lines[(empty, s.right, empty, s.right)]

            if y == height - 1:
                bottom += lines[(l.bottom, s.left, s.bottom, empty)]
                bottom += 3 * lines[(s.bottom, empty,  s.bottom, empty)]  # Multiply by content width
                if x == width - 1:
                    bottom += lines[(s.bottom, s.right, empty, empty)]

        print(top)
        print(middle)
        if bottom:
            print(bottom)


# Simplify to avoid thinking too much
formats = [
    ["elll", "lhlh", "llel"],
    ["L", "lhlh", "L"],
    ["hlhl", "H", "hlhl"]
]

contents = [
    ["Hello", "world", "!"],
    ["Foo", "bar", "baz"]
]

draw_box(formats, contents)
