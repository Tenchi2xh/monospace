from enum import Enum
from math import sqrt
from typing import List
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
        ratio = original.height / original.width
        image = original.resize(
            (width, int(width * ratio)),
            resample=Image.LANCZOS
        )
    else:
        image = original

    pixels = image.convert("RGBA").load()
    lines = []

    def n_closest_color(n, color, palette):
        n_closest = nsmallest(
            n, palette,
            key=lambda k: distance(color, palette[k])
        )
        return [palette[closest] for closest in n_closest]

    def color_tag(pixels, x, y, palette, background=False):
        r, g, b, _ = pixels[x, y]
        if palette != Palette.RGB:
            r, g, b = n_closest_color(1, (r, g, b), palettes[palette])[0]
        hex_color = rgb_to_hex(r, g, b)
        return FormatTag(
            kind=F.BackgroundColor if background else F.ForegroundColor,
            data={"color": hex_color}
        )

    def average_color(pixels, x, y):
        c1 = pixels[x, y]
        c2 = pixels[x, y + 1]
        return [int(0.5 * (c1[i] + c2[i])) for i in range(3)]

    # If height is odd, forget about the last line
    for y in range(0, image.height - (image.height % 2), 2):
        line = []
        for x in range(image.width):
            if mode == Mode.Super:
                pass

            elif mode == Mode.Pixels:
                t1 = color_tag(pixels, x, y, palette, background=True)
                t2 = color_tag(pixels, x, y + 1, palette)
                line.extend([t1, t2, "▄", t2.close_tag, t1.close_tag])

            elif mode == Mode.Dithered and palette != Palette.RGB:
                c0 = average_color(pixels, x, y)
                c1, c2 = n_closest_color(2, c0, palettes[palette])

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

            else:
                c = average_color(pixels, x, y)
                if palette != Palette.RGB:
                    c = n_closest_color(1, c, palettes[palette])[0]
                h = rgb_to_hex(*c)
                t = FormatTag(kind=F.ForegroundColor, data={"color": h})
                line.extend([t, "█", t.close_tag])
        lines.append(format_func(line))

    return lines


def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)
