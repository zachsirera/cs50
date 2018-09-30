from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    lines_a = set(a.split("\n"))
    lines_b = set(b.split("\n"))

    return lines_a & lines_b


def sentences(a, b):
    """Return sentences in both a and b"""

    sentences_a = set(sent_tokenize(a))
    sentences_b = set(sent_tokenize(b))

    return sentences_a & sentences_b


def substring_split(str, n):
    # Function in helpers.py to split strings into substrings of length n
    substrings = []

    for i in range(len(str) - n + 1):
        substrings.append(str[i: i + n])

    return substrings


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    substrings_a = set(substring_split(a, n))
    substrings_b = set(substring_split(b, n))

    return substrings_a & substrings_b