import pyphen
import random
random.seed(1337)

pyphen_dictionary = pyphen.Pyphen(lang="en_US")
wrap = pyphen_dictionary.wrap

# TODO: Language in context object?
# TODO: Inline ANSI escape sequence styles

def justify(text, width=80, offset=0):
    words = text.split()[::-1]
    words[-1] = " " * offset + words[-1]
    lines = [[]]

    def room_left(line):
        return width - (len(line) + sum(len(word) for word in line))

    while words:
        word = words.pop()

        line = lines[-1]
        available = room_left(line)

        if len(word) <= available:
            lines[-1].append(word)
        else:
            hyphenized = wrap(word, available)

            if hyphenized:
                lines[-1].append(hyphenized[0])
                lines.append([hyphenized[1]])
            else:
                lines.append([word])

    result = ""
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            spaces_to_add = room_left(line) + 1
            candidates = range(len(line) - 1)  # - 1 because we don't want to
                                               # add a space after the last word

            offsets = random.sample(candidates, spaces_to_add)
            for offset in offsets:
                line[offset] = line[offset] + " "

        spaced = " ".join(line)

        result += spaced
        result += "\n"

    return result


if __name__ == "__main__":
    paragraphs = [
        "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful.",
        "Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?",
        "On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish."
    ]

    width = 56
    empty = "     │ " + " " * width + " │"
    for p in paragraphs:
        print(empty)
        justified = justify(p, width=56, offset=3).splitlines()
        for line in justified:
            print("     │ " + line + (width - len(line)) * " " + " │")
    print(empty)
