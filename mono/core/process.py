from .domain import document
from pandocfilters import walk
from dataclasses import dataclass


@dataclass
class Unprocessed:
    kind: str


class Metadata(object):
    def __init__(self, metadata):
        self.identifier = metadata[0]
        self.classes = metadata[1]
        self.attributes = dict(metadata[2])


class Processor(object):
    def __init__(self, ast):
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

    def find_references(self, elements):
        references = {}
        for element in elements:
            if element["t"] == "Header":
                identifier = Metadata(element["c"][1]).identifier
                title = self.process_elements(element["c"][2])
                assert identifier not in references,\
                    "A header with this title already exists: %s" % title
                references[identifier] = title
        return references

    def process_elements(self, elements):
        processed = [
            self.process_node(e["t"], e["c"] if "c" in e else None)
            for e in elements
        ]
        return [pe for pe in processed if pe is not None]

    def process_node(self, kind, value):
        # --- Structural ------------------------------------------------------
        if kind == "Header":
            return self.process_header(value)
        elif kind == "Para":
            return self.process_paragraph(value)
        elif kind == "BlockQuote":
            return self.process_quote(value)
        elif kind == "OrderedList":
            return document.OrderedList(
                [self.process_elements(elements) for elements in value[1]])
        elif kind == "BulletList":
            return document.UnorderedList(
                [self.process_elements(elements) for elements in value])
        # --- Textual ---------------------------------------------------------
        elif kind == "Str":
            return value
        elif kind == "Strong":
            return document.Bold(self.process_elements(value))
        elif kind == "Emph":
            return document.Italic(self.process_elements(value))
        elif kind == "Link":
            return self.process_link(value)
        elif kind == "Space":
            return None

        return Unprocessed(kind)

    def make_text(self, elements):
        return document.Text(
            elements=self.process_elements(elements),
            notes=[]  # TODO: populate this
        )

    def process_paragraph(self, value):
        return document.Paragraph(self.make_text(value))

    def process_quote(self, value):
        return document.Quote(self.make_text(value))

    def process_header(self, value):
        level = value[0]
        metadata = Metadata(value[1])

        if "subtitle" in metadata.attributes:
            subtitle = document.Text(metadata.attributes["subtitle"].split())

        text = self.make_text(value[2])

        assert level in (1, 2, 3), "Hedings must be of level 1, 2 or 3"
        if level == 1:
            return document.Chapter(title=text)
        elif level == 2:
            # TODO:
            return document.SubChapter(title=text, subtitle=subtitle)
        else:
            return document.Section(title=text)

    def process_link(self, value):
        if value[2] and value[2][0].startswith("#"):
            identifier = value[2][0][1:]
            assert identifier in self.cross_references,\
                "Link points to unknown reference '%s'" % identifier
            return document.CrossRef(
                identifier=identifier,
                title=self.cross_references[identifier]
            )
        else:
            return Unprocessed("TrueLink")


def process(ast):
    meta = ast["meta"]
    processor = Processor(ast)
    cross_references = processor.cross_references
    document_elements = processor.processed

    return cross_references, document_elements
