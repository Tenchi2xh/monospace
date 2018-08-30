from .util.lang import auto_properties, auto_repr


@auto_repr
class TableSettings(object):
    @auto_properties
    def __init__(self,
        table_of_contents=None,
        list_of_figures=None,
        list_of_tables=None,
        list_of_code_listings=None,
        chapter_numbering=True,
        fill_character=".",
        fill_spacing=1
    ): pass


@auto_repr
class BookSettings(object):
    @auto_properties
    def __init__(self,
        tables=None,
        size=(80, 120),
        chapter_numbering=True,
        code_listings_line_numbering=True,
        code_listings_syntax_highlighting=True,
    ): pass


@auto_repr
class NumberMappers(object):
    default = lambda n: str(n)
    @property
    def roman(self): raise NotImplementedError()
    @property
    def roman_lower(self): raise NotImplementedError()
    @property
    def alphabetical(self): raise NotImplementedError()


@auto_repr
class HeaderFooter(object):
    # TODO: In two-sided mode, flip sides
    @auto_properties
    def __init__(self,
        left_cell_writer=None,
        middle_cell_writer=None,
        right_cell_writer=None,
        separator_line=False
    ): pass

    @staticmethod
    def with_page_number(
        left_cell_writer=None,
        middle_cell_writer=None,
        right_cell_writer=None,
        page_number_mapper=NumberMappers.default,
        center_page_number=False
    ):
        page_number_writer = lambda context: page_number_mapper(context.page_number)

        if center_page_number:
            return HeaderFooter(left_cell_writer, page_number_writer, right_cell_writer)
        else:
            return HeaderFooter(left_cell_writer, center_page_number, page_number_writer)


@auto_repr
class PageSettings(object):
    @auto_properties
    def __init__(self,
        margins=(5, 2, 5, 2),
        header=None, footer=None,
        two_sided=True,
        page_number=True,
        page_number_mapper=NumberMappers.default,
        center_page_number=False
    ):
        if page_number:
            if footer:
                self.footer = HeaderFooter.with_page_number(
                    left_cell_writer=footer.left_cell_writer,
                    middle_cell_writer=footer.middle_cell_writer,
                    right_cell_writer=footer.right_cell_writer,
                    page_number_mapper=page_number_mapper,
                    center_page_number=center_page_number
                )
            else:
                self.footer = HeaderFooter.with_page_number(
                    page_number_mapper=page_number_mapper,
                    center_page_number=center_page_number
                )
