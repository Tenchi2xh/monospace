
def ansi(*args):
    csi = "\033["
    return "%s%sm" % (csi, ";".join(map(str, args)))

def convert(tag, color=True):
    code = ""
    if tag.type == "Strong":
        code = ansi(1) if tag.start else ansi(22)
    elif tag.type == "Emphasis":
        code = ansi(3) if tag.start else ansi(23)
    elif tag.type == "Link":
        code = ansi(4) if tag.start else ansi(24)
    elif tag.type == "InlineCode":
        code = ansi(7) if tag.start else ansi(27)
    else:
        print("MISSING: " + tag.type)
        return ""

    if not color:
        return code

    if tag.type == "Strong":
        code += ansi(38, 5, 215) if tag.start else ansi(39)
    elif tag.type == "Emphasis":
        code += ansi(38, 5, 117) if tag.start else ansi(39)
    elif tag.type == "Link":
        code += ansi(38, 5, 152) if tag.start else ansi(39)

    return code
