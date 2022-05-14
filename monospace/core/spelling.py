import os
import re
from pathlib import Path

from leet.logging import log, log_progress
from spellchecker import SpellChecker

from ..util import flatten

spell = SpellChecker()


def check_spelling(path, settings):
    log.info(f"Checking the spelling of '{path}'...")
    if os.path.isdir(path):
        all_markdown = sorted(Path(path).rglob("*.md"))
        for file in log_progress.debug(all_markdown):
            _check_file(file, settings)
    else:
        _check_file(path, settings)


def _check_file(file, settings):
    with open(file, "r") as f:
        lines = _unmarkdown1(f.read()).splitlines()

    for i, line in enumerate(lines):
        words = _get_words(line)
        misspelled = spell.unknown(words)
        for word in misspelled:
            if word.lower() in settings.dictionary:
                continue
            candidates = spell.candidates(word)
            if len(candidates) <= 1:
                log.warn(
                    f"{file}:{i + 1}: unknown word '{word}'. "
                    "You might want to add it to the dictionary."
                )
            else:
                formatted_candidates = ", ".join(f"'{w}'" for w in candidates)
                log.warn(
                    f"{file}:{i + 1}: '{word}' is misspelled. "
                    f"Did you mean: {formatted_candidates}?"
                )


def _unmarkdown1(document):
    """Replace code blocks and yaml blocks with the same number of lines but empty"""
    block_patterns = [
        r"---+(\n.*)+?\.\.\.",
        r"```.*(\n.*)+?```",
        r"\[//\]: # \(ignore-spelling\)(\n.*)+?\[//\]: # \(/ignore-spelling\)",
    ]
    for pattern in block_patterns:
        for match in re.finditer(pattern, document):
            block = match.group(0)
            lines = block.splitlines()
            document = document.replace(block, "\n" * len(lines))
    return document


def _unmarkdown2(line):
    # Ignore horizontal rules, divs
    ignore_patterns = [
        r"^--+$",
        r"^::::.*$",
    ]
    for pattern in ignore_patterns:
        if re.match(pattern, line):
            return ""

    # Remove verbatim inline blocks
    line = re.sub(r"\`(.+?)\`", " ", line)
    # Remove single quotes aruond words (we want to keep apostrophes for contractions)
    line = re.sub(r"'(.+?)'", r"\1", line)
    # Remove link/image targets but keep caption
    line = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", line)
    # Remove things that look like URLs
    line = re.sub(r"\w+\.\w+\.\w+", " ", line)
    # Remove non word characters, keep essentials
    line = re.sub(r"[^\w\s'-]", " ", line)

    return line


def _get_words(line):
    words = _unmarkdown2(line).strip().split()
    unhyphened = flatten(w.split("-") for w in words)
    nonempty = filter(None, unhyphened)
    return nonempty
