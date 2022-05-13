from __future__ import print_function

import json
import sys

import fontforge

with open(sys.argv[1], "r") as f:
    config = json.load(f)


def extend_font(style, path_base, extensions):
    base = fontforge.open(path_base)

    for extension in extensions:
        font = fontforge.open(extension["files"][style])
        for _range in extension["ranges"]:
            from0 = int(_range["from"][0], 16)
            from1 = int(_range["from"][1], 16)
            to0 = int(_range["to"][0], 16)
            to1 = int(_range["to"][1], 16)

            font.selection.select(("unicode", "ranges"), from0, from1)
            font.copy()
            base.selection.select(("unicode", "ranges"), to0, to1)
            base.paste()

    elements = base.fontname.split("-")
    elements.insert(1, "Plus")
    base.fontname = "-".join(elements)
    base.generate("iosevka-plus-%s.t42" % style, flags=("apple"))


for style, path_base in config["bases"].iteritems():
    extend_font(style, path_base, config["extensions"])
