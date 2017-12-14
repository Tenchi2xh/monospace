from .util.lang import auto_repr

@auto_repr
class Context(object):
    def __init__(self, book):
        self.book = book
        self.stack = []
        self.chapter = [0 for _ in range(10)]
