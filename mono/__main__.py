import click

from .book import Book
from .layout import PageSettings, TableSettings, NumberMappers, BookSettings
from .viewer import view
from .util.lang import indent_json_like
from .compiler import compile


@click.command()
@click.argument("book_path", type=click.Path(exists=True))
def main(book_path):
    toc_settings = PageSettings(
        margins = (10, 4, 10, 4),
        page_number_mapper=NumberMappers.roman_lower,
        center_page_number=True
    )

    book = Book(
        path=book_path,
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


    elements = compile(book)

    #print(indent_json_like(repr(book)))
    #print(elements)

    #view(book)



if __name__ == "__main__":
    main()