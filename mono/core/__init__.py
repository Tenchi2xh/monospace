from .parse import parse
from .process import process
from .prerender import prerender
from .render import render

__all__ = ["parse", "process", "prerender", "render"]

"""Rendering pipeline for books

    .─────────────.
   ( markdown file )
    `─────────────'
           │
        parse()
           │
           ▼
    ┌────────────┐    Pandoc's AST is quite granular,
    │ Pandoc AST │    is a bit hard to navigate,
    └────────────┘    and contains too much information.
           │
       process()
           │
           ▼
     ┌──────────┐     This AST is much flatter,
     │ mono AST │     and the data is laid out in a way
     └──────────┘     that will make it easier to render.
           │
      prerender()
           │
           ▼
     ┌──────────┐
     │ rendered │     These blocks of text are completely rendered
     │  blocks  │     and only need to be set on a page.
     └──────────┘
           │
       render()       Page breaks, side notes, etc.
           │
           ▼
     ┏━━━━━━━━━━┓
     ┃ rendered ┃
     ┃   book   ┃
     ┗━━━━━━━━━━┛
"""
