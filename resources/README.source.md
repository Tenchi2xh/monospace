---
github-anchors: true
...

# Monospace

![](logo)

Contents:

1. [](#installation)
1. [](#usage)
1. [](#markdown-format)
    1. [](#settings)
    1. [](#standard-markdown)
    1. [](#pandoc-features)
    1. [](#custom-elements)
1. [](#setting-up-a-development-environment)
    1. [](#poetry)
    1. [](#git-hook)
    1. [](#sublime-text)
    1. [](#custom-repl)
    1. [](#building-the-fonts)

TOWRITE: Intro

## Installation {subtitle="Where the magic starts"}

This project _requires_ [Python 3.7.0](https://www.python.org/downloads/release/python-370/) or later.

To install, run:

```bash
pip install monospace
```

## Usage {subtitle="RTFM"}

For now, Monospace only comes with one command, `typeset`:

```plain
Usage: monospace typeset [OPTIONS] MARKDOWN_FILE

  Typeset a markdown file into a book.

  Saves the formatted book in the same directory as the input file.

Options:
  -t, --to [ansi|html|ps|pdf]  Destination format.  [required]
  -p, --preview                Do not save a file,
                               just print to stdout.
  -O, --open                   Open output file.
  -l, --linear                 Produce only one long page.
  --help                       Show this message and exit.
```

Example usages:

- Typeset a file and preview the result in a terminal:

    ```bash
    monospace typeset file.md --to ansi --preview
    ```
- Typeset a file into a contiguous html document, `readme.html`:

    ```bash
    monospace typeset README.md --linear --to html
    ```
- Typeset a file into a PDF book and open the result:

    ```bash
    monospace typeset my_book.md --to pdf --open
    ```

## Markdown format {subtitle="The nitty-gritty"}

TOWRITE

### Settings

TOWRITE

### Standard Markdown

TOWRITE

### Pandoc features

TOWRITE

### Custom elements

TOWRITE

## Setting up a development environment {subtitle="“So that they rhyme” — G. Lucas"}

TOWRITE

### Poetry

This project is managed and packaged by a promising relatively new tool, [Poetry](https://github.com/sdispater/poetry/). The package information and dependencies are declared in the `pyproject.toml` file, introduced in [PEP 518](https://www.python.org/dev/peps/pep-0518/).

To install Poetry, run:

```bash
pip install poetry
```

Poetry installs all dependencies in an isolated [virtual environment](https://docs.python.org/3/tutorial/venv.html). By default, this virtual environment is created somewhere outside of the project directory, but it is more convenient to have it inside, so that IDEs like Sublime Text can use linters and type checkers from within the virtual environment:

```bash
poetry settings.virtualenvs.in-project true
```

We can now install the project dependencies, including development dependencies:

```bash
poetry install
```

To run commands in the virtual environment, it is possible to use `poetry run` or `poetry shell`, however these are not very convenient. Instead, we can [activate](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) it:

```bash
source .venv/bin/activate
```

After activating, commands like `pip` and `python` are all run with the version specific to this project, including dependencies. Development dependencies also become available, such as the commands `pytest`, `flake8` and `mypy`.

To avoid having to remember how to activate the virtual environment, here is useful alias to put in your bash configuration:

```
alias pactivate='source $(poetry show -v | sed -n 1p | sed "s/^.*: \(.*\)$/\1/")/bin/activate'
```

This will activate the virtual environment for the current Poetry project (works also from a sub-directory inside that project).

### Git hook

To ensure a standard of quality, the code of this project is checked with `flake8` and `mypy`. They are part of the development dependencies in the project definition, and can be run inside the virtual environment.

The script `scripts/check.sh` can be run to quickly check everything, and a [git hook](https://githooks.com/) is provided at `scripts/pre-commit`. To enable the hook, just copy the file to `.git/hooks`. The check will happen before each commit.

### Sublime Text

A `.sublime-project` file is provided to set up things around in [Sublime Text](https://www.sublimetext.com/):

- Configuration for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter): if you have [SublimeLinter-contrib-mypy](https://github.com/fredcallaway/SublimeLinter-contrib-mypy) and [SublimeLinter-flake8](https://github.com/SublimeLinter/SublimeLinter-flake8) installed, it will configure them to point to the virtual environment's executables.
- A few ignored folders to hide some things covered in the `.gitignore` file.

### Custom REPL

TOWRITE

### Building the fonts

TOWRITE
