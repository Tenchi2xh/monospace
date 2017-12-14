import os

from .layout import *
from .parser import parse_markdown
from .util.lang import auto_repr


@auto_repr
class Book(object):
    def __init__(self, path, book_settings, default_page_settings):
        if os.path.isfile(path):
            with open(path, "r") as f:
                self.document = f.read()
        elif os.path.isdir(path):
            files = sorted([os.path.join(path, file) for file in os.listdir(path)])
            fragments = []
            for file in files:
                with open(file, "r") as f:
                    fragments.append(f.read())
            self.document = "\n".join(fragments)
        else:
            raise IOError("Path %s not found" % path)

        self.book_settings = book_settings
        self.default_page_settings = default_page_settings
        self.ast = parse_markdown(self.document)
