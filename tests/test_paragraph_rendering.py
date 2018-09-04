from monospace.core.rendering.paragraph import align, Alignment, flatten
from monospace.core.domain import document as d, Settings
from monospace.core.formatting import HtmlFormatter, FormatTag, Format as F

s = d.space


# https://stackoverflow.com/a/6300649
def intersperse(sequence, value):
    result = [value] * (2 * len(sequence) - 1)
    result[::2] = sequence
    return result


def test_flatten():
    elements = [
        "This", s, "text", s, "contains", s, "mixed", s, "styles:", s,
        d.Bold([
            "Hello,", s,
            d.Italic(["World!"])
        ])
    ]
    expected = [
        "This", s, "text", s, "contains", s, "mixed", s, "styles:", s,
        FormatTag(F.Bold, open=True),
        "Hello,", s,
        FormatTag(F.Italic, open=True),
        "World!",
        FormatTag(F.Italic, open=False),
        FormatTag(F.Bold, open=False)
    ]

    assert flatten(elements) == expected


def test_plain_paragraph_rendering():
    text = "Smile spoke total few great had never their too. Amongst moments do in arrived at my replied. Fat weddings servants but man believed prospect. Companions understood is as especially pianoforte connection introduced. Nay newspaper can sportsman are admitting gentleman belonging his. Is oppose no he summer lovers twenty in. Not his difficulty boisterous surrounded bed. Seems folly if in given scale. Sex contented dependent conveying advantage can use."  # noqa
    words = intersperse(text.split(), d.space)
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
    text = [
        "Yet", s, "bed", s,
        d.Bold([
            "any", s, "for", s,
            d.Italic([
                "travelling", s, "assistance",
            ]),
            s, "indulgence", s, "unpleasing", s, "foobar.",
        ]),
        s, "Not", s, "thoughts", s,
        d.Bold(["all", s, "exercise", s, "blessing."])
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
        "<b><i>elling assistance</i> in-</b>",
        "<b>dulgence unpleasing</b>  ",
        "<b>foobar.</b> Not thoughts ",
        "<b>all exercise bless-</b>  ",
        "<b>ing.</b>                 ",
    ]

    settings = Settings.from_meta({}, "")
    format_func = lambda t: HtmlFormatter.format_tags(t, settings)  # noqa

    unformatted = align(text, Alignment.left, width)
    formatted = align(text, Alignment.left, width, format_func=format_func)

    assert unformatted == expected_unformatted
    assert formatted == expected_formatted


def test_punctuation_after_tag():
    text = [
        "Hello,", s,
        d.Bold([
            "World"
        ]),
        "!"
    ]

    settings = Settings.from_meta({}, "")
    format_func = lambda t: HtmlFormatter.format_tags(t, settings)  # noqa

    expected = ["Hello, <b>World</b>! "]

    assert align(text, Alignment.left, 14, format_func=format_func) == expected


def ignore_test_punctuation_on_new_line():
    text = ["Hello,", s, d.Bold(["World"]), "!"]
    expected = [
        "Hello,      ",
        "World!      "
    ]
    assert align(text, Alignment.left, 12) == expected
