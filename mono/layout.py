from .util.lang import auto_properties


class TableSettings(object):
    @auto_properties
    def __init__(self,
        table_of_contents=False,
        list_of_figures=False,
        list_of_tables=False,
        list_of_code_listings=False,
        chapter_numbering=True,
        fill_character=".",
        fill_spacing=1
    ): pass


class BookSettings(object):
    @auto_properties
    def __init__(self,
        tables=None,
        chapter_numbering=True,
        code_listings_line_numbering=True,
        code_listings_syntax_highlighting=True,
    ): pass


class NumberMappers(object):
    default = lambda n: str(n)
    roman = raise NotImplementedError()
    roman_lower = raise NotImplementedError()
    alphabetical = raise NotImplementedError()


class HeaderFooter(object):
    # TODO: In two-sided mode, flip sides
    @auto_properties
    def __init__(self,
        left_cell_writer=None,
        middle_cell_writer=None,
        right_cell_writer=None
    ): pass

    @staticmethod
    def with_page_number(self,
                        left_cell_writer=None,
                        middle_cell_writer=None,
                        right_cell_writer=None,
                        page_number_mapper=NumberMappers.default,
                        center_page_number=False):

        page_number_writer = lambda context: page_number_mapper(context.page_number)

        if center_page_number:
            return HeaderFooter(left_cell_writer, page_number_writer, right_cell_writer)
        else:
            return HeaderFooter(left_cell_writer, center_page_number, page_number_writer)


class PageSettings(object):
    @auto_properties
    def __init__(self,
        size=(80, 120),
        marigns=(5, 2, 5, 2),
        header=None, footer=None,
        two_sided=True,
        page_number=True,
        page_number_mapper=NumberMappers.default,
        center_page_number=False
    ): pass
