from .formatter import Formatter


def csi(params, end):
    return "\033[%s%s" % (";".join(str(p) for p in params), end)


codes = {
    "Bold": (csi([1], "m"), csi([22], "m")),
    "Italic": (csi([3], "m"), csi([23], "m")),
}


class AnsiFormatter(Formatter):
    @staticmethod
    def format_tag(tag):
        return codes.get(tag.kind, ("", ""))[int(not tag.open)]
