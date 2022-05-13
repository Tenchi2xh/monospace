from typing import Any, Dict, List, Optional

from ..util import intersperse
from .domain import Settings
from .domain import document as d
from .formatting import styles
from .symbols.characters import double_quotes, single_quotes


def process(ast: dict, working_dir):
    meta = process_meta(ast["meta"])
    settings = Settings.from_meta(meta, working_dir)
    processor = Processor(ast, settings)

    cross_references = processor.cross_references
    document_elements = processor.processed

    return settings, cross_references, document_elements


class Processor(object):
    def __init__(self, ast: dict, settings: Settings) -> None:
        self.settings = settings
        self.note_count = -1
        self.cross_references = self.find_references(ast["blocks"])
        # FIXME: This is just for the mockup
        self.cross_references.update({
            "how-to-pay": "How to pay",
            "table-of-contents": "Table of contents",
            "body-text": "Body text",
            "point-size": "Point size",
            "line-spacing": "Line spacing",
            "line-length": "Line length",
            "page-margins": "Page margins",
            "typewriter-habit": "Typewriter habit",
            "system-fonts": "System fonts",
            "free-fonts": "Free fonts",
            "font-recommendations": "Font recommendations",
            "times-new-roman": "Times New Roman",
            "arial": "Arial",
            "summary-of-key-rules": "Summary of key rules",
        })
        self.processed = self.process_elements(ast["blocks"])

    def find_references(self, elements: list) -> Dict[str, str]:
        references: Dict[str, str] = {}
        for element in elements:
            if element["t"] == "Header":
                identifier = Metadata(element["c"][1]).identifier
                title = join(self.process_elements(element["c"][2]))
                assert identifier not in references,\
                    "A header with this title already exists: %s" % title
                references[identifier] = title
        self.note_count = -1
        return references

    def process_elements(self, elements) -> List[d.Element]:
        processed = [
            self.process_element(e["t"], e["c"] if "c" in e else None)
            for e in elements
        ]
        return [pe for pe in processed if pe is not None]

    def process_element(self, kind: str, value: Any) -> Optional[d.Element]:
        # --- Structural ------------------------------------------------------
        if kind == "Header":
            return self.process_header(value)
        elif kind == "Para" or kind == "Plain":
            return self.process_paragraph(value)
        elif kind == "BlockQuote":
            return self.process_quote(value)
        elif kind == "OrderedList":
            return d.OrderedList(
                [self.process_elements(elements) for elements in value[1]])
        elif kind == "BulletList":
            return d.UnorderedList(
                [self.process_elements(elements) for elements in value])
        elif kind == "Div":
            return self.process_div(value)
        elif kind == "CodeBlock":
            language = "" if not value[0][1] else value[0][1][0]
            return d.CodeBlock(language=language, code=value[1])
        elif kind == "Image":
            return d.Image(
                uri=value[2][0],
                caption=d.Note(children=self.process_elements(value[1]), count=None),
                **dict(value[0][2])
            )
        elif kind == "HorizontalRule":
            return d.PageBreak()
        # --- Textual ---------------------------------------------------------
        elif kind == "Str":
            return value
        elif kind == "Strong":
            return d.Bold(children=self.process_elements(value))
        elif kind == "Emph":
            return d.Italic(children=self.process_elements(value))
        elif kind == "Link":
            return self.process_link(value)
        elif kind == "Code":
            return d.Code(stylize(value[1], styles.monospace))
        elif kind == "Quoted":
            return self.process_quoted(value)
        elif kind == "Note":
            return self.process_note(value)
        elif kind == "Space" or kind == "SoftBreak":
            return d.Space()

        return d.Unprocessed(kind)

    def make_text(self, elements):
        return d.Text(
            elements=self.process_elements(elements),
            notes=[]  # TODO: populate this
        )

    def process_paragraph(self, value):
        text = self.make_text(value)
        if any(isinstance(e, d.Image) for e in text.elements):
            if len(text.elements) != 1:
                raise ValueError("Inline images are not supported")
            return text.elements[0]
        return d.Paragraph(text)

    def process_note(self, value):
        self.note_count += 1
        elements = self.process_elements(value)
        assert len(elements) == 1 and isinstance(elements[0], d.Paragraph)
        children = elements[0].text.elements
        return d.Note(  # type: ignore
            children=children,
            count=self.note_count
        )

    def process_quote(self, value):
        # Quote text elements are wrapped in a paragraph
        return d.Quote(self.make_text(value).elements[0].text)

    def process_header(self, value):
        level = value[0]
        metadata = Metadata(value[1])

        subtitle = None
        if "subtitle" in metadata.attributes:
            subtitle = d.Text(
                elements=intersperse(
                    metadata.attributes["subtitle"].split(),
                    d.Space()
                )
            )

        title = self.make_text(value[2])
        title_string = join([title])
        id = next(
            k for k, v in self.cross_references.items()
            if v == title_string
        )

        assert level in (1, 2, 3), "Hedings must be of level 1, 2 or 3"
        if level == 1:
            return d.Chapter(title=title, identifier=id)
        elif level == 2:
            return d.SubChapter(title=title, subtitle=subtitle, identifier=id)
        else:
            return d.Section(title=title, identifier=id)

    def process_link(self, value):
        if not value[2]:
            raise ValueError("Missing URI for link %s" % value)

        identifier = value[2][0]
        title = join(self.process_elements(value[1]))

        if identifier.startswith("#"):
            assert identifier[1:] in self.cross_references,\
                "Link points to unknown reference '%s'" % identifier
            title = self.cross_references[identifier[1:]]
            if self.settings.github_anchors:
                identifier = "#user-content-" + identifier[1:]

        formatted_title = stylize(title, styles.small_caps)
        return d.CrossRef(
            children=formatted_title,
            identifier=identifier
        )

    def process_quoted(self, value):
        quotes = double_quotes
        if value[0]["t"] == "SingleQuote":
            quotes = single_quotes

        elements = self.process_elements(value[1])
        return d.Quoted(children=[quotes[0]] + elements + [quotes[1]])

    def process_div(self, value):
        kind = value[0][1][0]
        if kind == "Aside":
            return d.Aside(self.process_elements(value[1]))
        else:
            return d.Unprocessed("Div:" + kind)


class Metadata(object):
    def __init__(self, metadata):
        self.identifier: str = metadata[0]
        self.classes: List[str] = metadata[1]
        self.attributes: Dict[str, str] = dict(metadata[2])


def join(elements: List[d.Element]) -> str:
    def do_join(elements):
        result = []
        for element in elements:
            if isinstance(element, str):
                result.append(element)
            elif isinstance(element, d.Note):
                continue
            elif hasattr(element, "elements"):
                result.extend(do_join(element.elements))
            elif hasattr(element, "list_elements"):
                for _elements in element.list_elements:
                    result.extend(do_join(_elements))
            elif hasattr(element, "children"):
                result.extend(element.children)
        return result

    return " ".join(do_join(elements))


def process_meta(meta: dict) -> dict:
    result: dict = {}
    for k, v in meta.items():
        kind = v["t"]
        content = v["c"]

        if kind == "MetaMap":
            result[k] = process_meta(content)
        elif kind == "MetaInlines":
            value = ""
            for elem in content:
                if elem["t"] == "Str":
                    value += elem["c"]
                elif elem["t"] == "Space":
                    value += " "
                else:
                    raise TypeError("Unknown meta value type: %s" % elem["t"])
            try:
                result[k] = int(value)
            except ValueError:
                try:
                    result[k] = float(value)
                except ValueError:
                    result[k] = value
        elif kind == "MetaBool":
            result[k] = content
    return result


def stylize(text, style):
    words = text.split()
    result = []
    for word in words:
        result.append(style(word))
        result.append(d.Space())
    result.pop()
    return result
