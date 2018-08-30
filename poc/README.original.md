# About **Mono**

**Mono** is a tool for *parsing*, *typesetting* and *rendering* a set of [Markdown](https://daringfireball.net/projects/markdown/syntax) files into a book, with multiple output formats: for now, a live terminal view using [ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code), and HTML (output of which you are presently reading!)

## Why?

After writing a fair amount of *esoteric graphical terminal experiments*, such as [Almonds](https://github.com/Tenchi2xh/Almonds), [cursebox](https://github.com/Tenchi2xh/cursebox) and [Scurses](https://github.com/Tenchi2xh/Scurses), and after being surprised with the great reception of my [Devoxx Belgium talk](https://www.youtube.com/watch?v=j5zA5Xi_ph8), I have found myself wanting to try and write a *small* book, codenamed *"Project Codex"*, about the history of terminals and the various techniques I have discovered or developed.

For now, developping **Mono** is a fun challenge in itself – the writing will come later, if at all.

## Running

For now, running `main` with a Markdown file renders it in a paragraph:

**python -m mono codex/test.md**

And, to generate the readme:

**python -m mono.util.readme**

## Planned features

(*List rendering not yet implemented*)

- Text formatting:
    - Alignments (left, center, right, fully justified)
    - Smart hyphenation
    - Weights and colors
- Book features:
    - Title page
    - Table of contents, list of figures, tables, code listings
    - Syntax highlighted code blocks
    - Tables and figures
    - Footnotes and references
    - Multi-column mode
    - Page, chapter, tagble, figure, footnote numbering
    - Headers and footers
    - Smart pagination (paragraph breaking)
- Customization via metadata
    - Margins
    - Styles of numbering
