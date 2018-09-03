from typing import Optional, Any, Dict, List

from .domain import Settings
from .formatting import styles
from .domain import document as d
from .symbols.characters import double_quotes, single_quotes


def process(ast: dict, source_file):
    # TODO: Add support for settings for the typesetting and metadata
    meta = process_meta(ast["meta"])
    settings = Settings.from_meta(meta, source_file)
    processor = Processor(ast)

    cross_references = processor.cross_references
    document_elements = processor.processed

    return settings, cross_references, document_elements


class Processor(object):
    def __init__(self, ast: dict) -> None:
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
            "foreword": "Foreword",
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
            return d.Image(uri=value[2][0])
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
            return d.Code([styles.monospace(value[1])])
        elif kind == "Quoted":
            return self.process_quoted(value)
        elif kind == "Space":
            return d.space

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
        return d.Paragraph(self.make_text(value))

    def process_quote(self, value):
        return d.Quote(self.make_text(value))

    def process_header(self, value):
        level = value[0]
        metadata = Metadata(value[1])

        subtitle = None
        if "subtitle" in metadata.attributes:
            subtitle = d.Text(metadata.attributes["subtitle"].split())

        text = self.make_text(value[2])

        assert level in (1, 2, 3), "Hedings must be of level 1, 2 or 3"
        if level == 1:
            return d.Chapter(title=text)
        elif level == 2:
            return d.SubChapter(title=text, subtitle=subtitle)
        else:
            return d.Section(title=text)

    def process_link(self, value):
        if value[2] and value[2][0].startswith("#"):
            identifier = value[2][0][1:]
            assert identifier in self.cross_references,\
                "Link points to unknown reference '%s'" % identifier

            title = styles.small_caps(self.cross_references[identifier])
            return d.CrossRef(
                children=[title],
                identifier=identifier,
            )
        else:
            # Link's text: self.process_elements(value[1])
            return d.Unprocessed("TrueLink")

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
    return result
