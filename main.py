import re
import unicodedata


TRANSLATION_TABLE = str.maketrans({
    "“": '"', "”": '"', "„": '"', "‟": '"', "«": '"', "»": '"',
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "—": "-", "–": "-", "−": "-",
    "\u00A0": " ",
    "\u202F": " ",
})

RE_MULTISPACE = re.compile(r"[ \t]{2,}")


def is_weird_unicode(ch):
    if ch in ("\n", "\r", "\t"):
        return False
    return unicodedata.category(ch) in {"Cc", "Cf", "Co", "Cn"}

def clean_text(text):
    text = text.translate(TRANSLATION_TABLE)
    text = "".join(ch for ch in text if not is_weird_unicode(ch))
    lines = text.splitlines(keepends=True)
    cleaned = []
    for line in lines:
        if line.endswith(("\r\n", "\n", "\r")):
            if line.endswith("\r\n"):
                body, eol = line[:-2], "\r\n"
            else:
                body, eol = line[:-1], line[-1]
        else:
            body, eol = line, ""
        body = RE_MULTISPACE.sub(" ", body)
        cleaned.append(body + eol)
    return "".join(cleaned)


if __name__ == '__main__':
    with open("source.txt", "r", encoding="utf-8") as f:
        source = f.read()

    result = clean_text(source)

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(result)
