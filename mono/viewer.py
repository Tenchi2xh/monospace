from .cursebox import *
from .book import Book
from .layout import *
from .util.lang import indent_json_like


def view(book):
    with Cursebox() as cb:
        width, height = cb.width, cb.height



if __name__ == "__main__":
    import sys
    assert sys.argv[1]

    toc_settings = PageSettings(
        margins = (10, 4, 10, 4),
        page_number_mapper=NumberMappers.roman_lower,
        center_page_number=True
    )

    book = Book(
        sys.argv[1],
        book_settings = BookSettings(
            tables = TableSettings(
                table_of_contents     = toc_settings,
                list_of_figures       = toc_settings,
                list_of_tables        = toc_settings,
                list_of_code_listings = toc_settings,
                chapter_numbering = True,
                fill_character = ".",
                fill_spacing = 1
            )
        ),
        default_page_settings = PageSettings(
            margins = (5, 2, 5, 2),
            header = None,
            footer = None,
            two_sided = True,
            page_number = True,
            page_number_mapper=NumberMappers.default,
            center_page_number=False
        )
    )

    print(indent_json_like(repr(book)))
