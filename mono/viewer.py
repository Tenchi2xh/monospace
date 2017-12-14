from .cursebox import *


def view(book):
    with Cursebox() as cb:
        width, height = cb.width, cb.height

        cb.poll_event()
