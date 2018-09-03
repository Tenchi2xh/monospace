from typing import List
from PIL import Image  # type: ignore

from ..formatting import Formatter, Format as F, FormatTag

detailed = True


def ansify(uri: str, formatter: Formatter, width: int) -> List[str]:
    original = Image.open(uri)

    ratio = original.height / original.width
    image = original.resize(
        (width, int(width * ratio)),
        resample=Image.LANCZOS
    )

    pixels = image.convert("RGBA").load()
    lines = []

    for y in range(0, image.height, 2):
        line = []
        for x in range(image.width):
            r, g, b, _ = pixels[x, y]
            color = rgb_to_hex(r, g, b)
            t = FormatTag(kind=F.ForegroundColor, data={"color": color})

            if detailed and y + 1 < image.height:
                r2, g2, b2, _ = pixels[x, y + 1]
                color2 = rgb_to_hex(r2, g2, b2)
                # Flip, because we want to color the lower block
                t.kind = F.BackgroundColor
                t2 = FormatTag(kind=F.ForegroundColor, data={"color": color2})

                line.extend([t, t2, "▄", t2.close_tag, t.close_tag])
            else:
                line.extend([t, "█", t.close_tag])
        lines.append(formatter.format_tags(line))

    return lines


def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)
