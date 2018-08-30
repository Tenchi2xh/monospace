from ..book import Book
from ..layout import PageSettings, BookSettings
from ..compiler import compile
from ..formatting import html
from ..drawing.paragraph import align, Alignment
from ..util.lang import indent_json_like


logo = [
    " _____ ___ ___ ___ ",
    "|     | . |   | . |",
    "|_|_|_|___|_|_|___|",
    "",
    "A monospace book typesetter"
]


if __name__ == "__main__":
    book = Book(
        path="./README.original.md",
        book_settings = BookSettings(),
        default_page_settings = PageSettings()
    )

    elements = compile(book)
    #print(indent_json_like(str(book)))

    width = 50
    left = " " * 25 + "│ "
    right = " │"
    empty = left + " " * width + right
    result = []

    result.append("<pre>")
    result.append(empty)
    for i, line in enumerate(logo):
        w = len(line)
        ls = int((width - w) / 2)
        rs = width - w - ls
        if i == len(logo) - 1:
            line = "<i>%s</i>" % line
        result.append(left + " " * ls + line + " " * rs + right)

    for text, formatting, _ in elements:
        result.append(empty)
        aligned = align(
            text,
            alignment=Alignment.justify,
            width=width,
            offset=0,
            formatting=formatting,
            formatter=html
        ).splitlines()
        for line in aligned:
            result.append(left + line + (width - len(line)) * " " + right)
    result.append(empty)
    result.append("</pre>")

    with open("./README.md", "w") as f:
        f.write("\n".join(result))
