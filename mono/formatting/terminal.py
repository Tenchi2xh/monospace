
def convert(tag):
    csi = "\033["
    code = ""
    if tag.type == "Strong":
        code = "1m" if tag.start else "22m"
    elif tag.type == "Emphasis":
        code = "3m" if tag.start else "23m"
    elif tag.type == "Link":
        code = "4m" if tag.start else "24m"
    elif tag.type == "InlineCode":
        code = "7m" if tag.start else "27m"
    else:
        print("MISSING: " + tag.type)
        return ""

    return csi + code
