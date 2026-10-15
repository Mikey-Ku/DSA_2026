"""Needleman-Wunsch global sequence alignment
"""

MATCH = 1
MISMATCH = -1
GAP = -2


def score_grid(a: str, b: str, gap: int = GAP) -> list[list[int]]:
    """Fills the dynamic programming grid"""

    rows, cols = len(a) + 1, len(b) + 1
    grid = [[0] * cols for _ in range(rows)]

    # Lining up letters against nothing costs a gap each
    for i in range(rows):
        grid[i][0] = i * gap
    for j in range(cols):
        grid[0][j] = j * gap

    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                diagonal = grid[i - 1][j - 1] + MATCH
            else:
                diagonal = grid[i - 1][j - 1] + MISMATCH
            up = grid[i - 1][j] + gap    # letter of a against a gap
            left = grid[i][j - 1] + gap  # letter of b against a gap
            grid[i][j] = max(diagonal, up, left)
    return grid


def align(a: str, b: str, gap: int = GAP) -> tuple[int, str, str]:
    """Aligns a and b

    Returns:
        (score, aligned_a, aligned_b), where the aligned strings are the same
        length and "-" marks a gap
    """
    grid = score_grid(a, b, gap)

    aligned_a: list[str] = []
    aligned_b: list[str] = []
    i, j = len(a), len(b)
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            points = MATCH if a[i - 1] == b[j - 1] else MISMATCH
            if grid[i][j] == grid[i - 1][j - 1] + points:
                aligned_a.append(a[i - 1])
                aligned_b.append(b[j - 1])
                i -= 1
                j -= 1
                continue
        if i > 0 and grid[i][j] == grid[i - 1][j] + gap:
            aligned_a.append(a[i - 1])
            aligned_b.append("-")
            i -= 1
        else:
            aligned_a.append("-")
            aligned_b.append(b[j - 1])
            j -= 1

    aligned_a.reverse()
    aligned_b.reverse()
    return grid[len(a)][len(b)], "".join(aligned_a), "".join(aligned_b)


def match_line(aligned_a: str, aligned_b: str) -> str:
    """Returns a line with | under each matching letter, for printing"""
    line = ""
    for x, y in zip(aligned_a, aligned_b):
        line += "|" if x == y else " "
    return line
