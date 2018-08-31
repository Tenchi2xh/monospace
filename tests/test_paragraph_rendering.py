from mono.core.rendering.paragraph import align, Alignment, flatten
from mono.core.domain import document as d
from mono.core.formatting import Formatter, FormatTag


def test_flatten():
    elements = [
        "This", "text", "contains", "mixed", "styles:",
        d.Bold([
            "Hello,",
            d.Italic(["World!"])
        ])
    ]
    expected = [
        "This", "text", "contains", "mixed", "styles:",
        FormatTag("Bold", open=True),
        "Hello,",
        FormatTag("Italic", open=True),
        "World!",
        FormatTag("Italic", open=False),
        FormatTag("Bold", open=False)
    ]

    assert flatten(elements) == expected


def test_plain_paragraph_rendering():
    text = "Smile spoke total few great had never their too. Amongst moments do in arrived at my replied. Fat weddings servants but man believed prospect. Companions understood is as especially pianoforte connection introduced. Nay newspaper can sportsman are admitting gentleman belonging his. Is oppose no he summer lovers twenty in. Not his difficulty boisterous surrounded bed. Seems folly if in given scale. Sex contented dependent conveying advantage can use."  # noqa
    words = text.split()
    width = 40

    expected_left = [
        "Smile spoke total few great had never   ",
        "their too. Amongst moments do in arrived",
        "at my replied. Fat weddings servants but",
        "man believed prospect. Companions under-",
        "stood is as especially pianoforte con-  ",
        "nection introduced. Nay newspaper can   ",
        "sportsman are admitting gentleman be-   ",
        "longing his. Is oppose no he summer     ",
        "lovers twenty in. Not his difficulty    ",
        "boisterous surrounded bed. Seems folly  ",
        "if in given scale. Sex contented depen- ",
        "dent conveying advantage can use.       ",
    ]

    expected_right = [
        "   Smile spoke total few great had never",
        "their too. Amongst moments do in arrived",
        "at my replied. Fat weddings servants but",
        "man believed prospect. Companions under-",
        "  stood is as especially pianoforte con-",
        "   nection introduced. Nay newspaper can",
        "   sportsman are admitting gentleman be-",
        "     longing his. Is oppose no he summer",
        "    lovers twenty in. Not his difficulty",
        "  boisterous surrounded bed. Seems folly",
        " if in given scale. Sex contented depen-",
        "       dent conveying advantage can use.",
    ]

    expected_center = [
        " Smile spoke total few great had never  ",
        "their too. Amongst moments do in arrived",
        "at my replied. Fat weddings servants but",
        "man believed prospect. Companions under-",
        " stood is as especially pianoforte con- ",
        " nection introduced. Nay newspaper can  ",
        " sportsman are admitting gentleman be-  ",
        "  longing his. Is oppose no he summer   ",
        "  lovers twenty in. Not his difficulty  ",
        " boisterous surrounded bed. Seems folly ",
        "if in given scale. Sex contented depen- ",
        "   dent conveying advantage can use.    ",
    ]

    assert align(words, Alignment.left, width) == expected_left
    assert align(words, Alignment.right, width) == expected_right
    assert align(words, Alignment.center, width) == expected_center


def test_styled_paragraph_rendering():
    class TestFormatter(Formatter):
        @staticmethod
        def format_tag(tag):
            if tag.kind == "Bold":
                return "<b>" if tag.open else "</b>"
            elif tag.kind == "Italic":
                return "<i>" if tag.open else "</i>"

    text = [
        "Yet", "bed",
        d.Bold([
            "any", "for",
            d.Italic([
                "travelling", "assistance"
            ]),
            "indulgence", "unpleasing", "foobar.",
        ]),
        "Not", "thoughts",
        d.Bold(["all", "exercise", "blessing."])
    ]
    width = 21

    expected_unformatted = [
        "Yet bed any for trav-",
        "elling assistance in-",
        "dulgence unpleasing  ",
        "foobar. Not thoughts ",
        "all exercise bless-  ",
        "ing.                 ",
    ]

    expected_formatted = [
        "Yet bed <b>any for <i>trav-</i></b>",
        "<b><i>elling assistance </i>in-</b>",
        "<b>dulgence unpleasing</b>  ",
        "<b>foobar. </b>Not thoughts<b></b> ",  # See fixme
        "<b>all exercise bless-</b>  ",
        "<b>ing.</b>                 ",
    ]

    # FIXME: We generate a bit too many tags
    # Here a tag starts and ends because
    # "thoughts" is added to the line, then the open tag,
    # then "all" is too big to fit, so we wrap and the open tag stays.

    unformatted = align(text, Alignment.left, width)
    formatted = align(text, Alignment.left, width, formatter=TestFormatter)

    assert unformatted == expected_unformatted
    assert formatted == expected_formatted
