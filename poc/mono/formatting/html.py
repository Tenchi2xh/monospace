
def t(type, tag):
    return ("<%s>" if tag.start else "</%s>") % (type)


def convert(tag, color=True):
    code = ""
    if tag.type == "Strong":
        code = t("b", tag)
    elif tag.type == "Emphasis":
        code = t("i", tag)
    elif tag.type == "Link":
        code = "<a href=%s>" % tag.target if tag.start else "</a>"
    elif tag.type == "InlineCode":
        code = "" if tag.start else ""
    else:
        print("MISSING: " + tag.type)
        return ""

    return code
