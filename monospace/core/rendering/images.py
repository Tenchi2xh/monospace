from enum import Enum
from math import sqrt
from typing import List, Sequence
from heapq import nsmallest
from PIL import Image  # type: ignore
from typing import Callable, Optional
from cursebox.palette import generate_xterm_256, distance  # type: ignore

from ..formatting import Format as F, FormatTag

Mode = Enum("Mode", ["Blocks", "Dithered", "Pixels", "Super"])
Palette = Enum("Palette", ["Monochrome", "ANSI", "Xterm", "RGB"])

XTERM_256 = generate_xterm_256()
palettes = {
    Palette.Monochrome: {n: XTERM_256[n] for n in (0, 15)},
    Palette.ANSI: {n: XTERM_256[n] for n in range(16)},
    Palette.Xterm: XTERM_256,
}


def ansify(
    uri: str,
    format_func: Callable,
    mode: Mode = Mode.Pixels,
    palette: Palette = Palette.RGB,
    width: Optional[int] = None,
) -> List[str]:

    original = Image.open(uri)

    if width is not None:
        if mode == Mode.Super:
            width *= 2
        ratio = original.height / original.width
        image = original.resize(
            (width, int(width * ratio)),
            resample=Image.LANCZOS
        )
    else:
        image = original

    pixels = image.convert("RGBA").load()

    if mode == Mode.Super:
        render = superify
    elif mode == Mode.Pixels:
        render = pixelify
    elif mode == Mode.Dithered and palette != Palette.RGB:
        render = ditherify
    else:
        render = blockify

    return render(image, pixels, palette, format_func)


def superify(image, pixels, palette, format_func):
    lines = []
    for y in range(0, image.height - (image.height % 4), 4):
        line = []
        for x in range(0, image.width - (image.width % 2), 2):
            # We take 2x4 pixels ⣿
            original = [
                [pixels[x + i, y + j] for i in range(2)]
                for j in range(4)
            ]
            # We average the first and last two rows together
            # to get 2x2 pixels (four corners)
            corners = [
                average_color(original[i * 2][j], original[i * 2 + 1][j])
                for i in range(2)
                for j in range(2)
            ]
            levels = [brightness(corner) for corner in corners]
            average_level = average(levels)

            # Split corners in 2 groups, depending if they are
            # lighter or darker than the average brightness
            group_a: List[Sequence[int]] = []
            group_b: List[Sequence[int]] = []
            groups = {}
            for i in range(len(corners)):
                color = corners[i]
                if levels[i] < average_level:
                    group, letter = group_a, "a"
                else:
                    group, letter = group_b, "b"
                group.append(color)
                groups[color] = letter

            # Calculate the color for each group
            # (average of all colors in that group)
            color_a = average_color(*group_a)
            color_b = average_color(*group_b)

            if not color_a:
                block = " "
                color_a = (0, 0, 0)
            elif not color_b:
                block = "█"
                color_b = (0, 0, 0)
            else:
                pattern = "".join(
                    groups[corners[i]]
                    for i in range(len(corners))
                )
                # We have two colors: there's at least one on each
                # side of the averge distance, by nature of an average
                mapping = {
                    "aaab": "▛",
                    "aaba": "▜",
                    "aabb": "▀",
                    "abaa": "▙",
                    "abab": "▌",
                    "abba": "▚",
                    "abbb": "▘",
                    "baaa": "▟",
                    "baab": "▞",
                    "baba": "▐",
                    "babb": "▝",
                    "bbaa": "▄",
                    "bbab": "▖",
                    "bbba": "▗",
                }
                block = mapping[pattern]

            if palette != Palette.RGB:
                color_a = n_closest_color(1, color_a, palette)[0]
                color_b = n_closest_color(1, color_b, palette)[0]

            t_a = FormatTag(
                kind=F.ForegroundColor,
                data={"color": rgb_to_hex(*color_a)}
            )
            t_b = FormatTag(
                kind=F.BackgroundColor,
                data={"color": rgb_to_hex(*color_b)}
            )

            line.extend([t_a, t_b, block, t_a.close_tag, t_b.close_tag])

        lines.append(format_func(line))

    return lines


def pixelify(image, pixels, palette, format_func):
    lines: List[str] = []
    for y in range(0, image.height - (image.height % 2), 2):
        line = []
        for x in range(image.width):
            t1 = color_tag(pixels, x, y, palette, background=True)
            t2 = color_tag(pixels, x, y + 1, palette)
            line.extend([t1, t2, "▄", t2.close_tag, t1.close_tag])
        lines.append(format_func(line))
    return lines


def ditherify(image, pixels, palette, format_func):
    lines: List[str] = []
    for y in range(0, image.height - (image.height % 2), 2):
        line = []
        for x in range(image.width):
            c0 = average_color(pixels[x, y], pixels[x, y + 1])
            c1, c2 = n_closest_color(2, c0, palette)

            d01 = sqrt(distance(c0, c1))
            d12 = sqrt(distance(c1, c2))
            d02 = sqrt(distance(c0, c2))

            if d02 > d01 + d12 or d12 == 0:
                c2 = c1
                block = "█"
            else:
                factor = d01 / d12
                if factor >= 1:
                    factor = 0.99
                block = " ░▒▓▓"[int(factor * 5)]

            hex1, hex2 = rgb_to_hex(*c1), rgb_to_hex(*c2)
            t1 = FormatTag(kind=F.ForegroundColor, data={"color": hex2})
            t2 = FormatTag(kind=F.BackgroundColor, data={"color": hex1})
            line.extend([t1, t2, block, t2.close_tag, t1.close_tag])
        lines.append(format_func(line))
    return lines


def blockify(image, pixels, palette, format_func):
    lines: List[str] = []
    for y in range(0, image.height - (image.height % 2), 2):
        line = []
        for x in range(image.width):
            c = average_color(pixels[x, y], pixels[x, y + 1])
            if palette != Palette.RGB:
                c = n_closest_color(1, c, palette)[0]
            h = rgb_to_hex(*c)
            t = FormatTag(kind=F.ForegroundColor, data={"color": h})
            line.extend([t, "█", t.close_tag])
        lines.append(format_func(line))
    return lines


def n_closest_color(n, color, palette_name):
    palette = palettes[palette_name]
    n_closest = nsmallest(
        n, palette,
        key=lambda k: distance(color, palette[k])
    )
    return [palette[closest] for closest in n_closest]


def color_tag(pixels, x, y, palette, background=False):
    r, g, b, _ = pixels[x, y]
    if palette != Palette.RGB:
        r, g, b = n_closest_color(1, (r, g, b), palette)[0]
    hex_color = rgb_to_hex(r, g, b)
    return FormatTag(
        kind=F.BackgroundColor if background else F.ForegroundColor,
        data={"color": hex_color}
    )


def average(values):
    return sum(values) / len(values)


def rgb_to_hex(r, g, b, *args):
    return '#%02x%02x%02x' % (r, g, b)


def average_color(*colors):
    rgbs = zip(*colors)
    return tuple([int(average(comp)) for comp in rgbs])


def brightness(color):
    return sum(color[:3]) / 3
