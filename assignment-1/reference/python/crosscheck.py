"""
Print the next-word map the original Python builds for each line of a corpus.

The Kotlin port has a `crossCheck` task that prints the same normalised format,
so `reference/crosscheck.sh` can diff the two and show that the translation
preserved behaviour rather than merely passing tests that were written to match
it.
"""

import sys


def unescape(line: str) -> str:
    """
    Decode the \\n, \\t, and \\\\ escapes used in the shared corpus file.

    Args:
        line: A single raw line from the corpus.

    Returns:
        The source text the line represents.
    """
    result = []
    index = 0
    while index < len(line):
        if line[index] == "\\" and index + 1 < len(line):
            escape = line[index + 1]
            result.append({"n": "\n", "t": "\t", "\\": "\\"}.get(escape, "\\" + escape))
            index += 2
        else:
            result.append(line[index])
            index += 1
    return "".join(result)


def main() -> None:
    """Print one normalised line per word of per corpus entry."""
    sys.path.insert(0, sys.path[0] or ".")
    from markov import build_next_words, build_word_list

    corpus_path = sys.argv[1]
    with open(corpus_path, encoding="utf-8") as corpus_file:
        lines = corpus_file.read().split("\n")

    for case_number, raw_line in enumerate(lines):
        if raw_line == "":
            continue
        next_words = build_next_words(build_word_list(unescape(raw_line)))
        for word in sorted(next_words):
            successors = "|".join(sorted(next_words[word]))
            print(f"{case_number}\t{word}\t{successors}")


if __name__ == "__main__":
    main()
