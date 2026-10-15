"""Tests for Needleman-Wunsch alignment"""

import unittest

from needleman_wunsch import align, match_line, score_grid


class NeedlemanWunschTest(unittest.TestCase):
    """Checks the Wikipedia example, then small cases with gap -2"""

    def test_wikipedia_example(self) -> None:
        """Wikipedia's GATTACA / GCATGCU"""
        self.assertEqual(align("GATTACA", "GCATGCU"), (-1, "GATTACA", "GCATGCU"))

    def test_identical(self) -> None:
        """Every letter matches, +1 each"""
        self.assertEqual(align("ACGT", "ACGT"), (4, "ACGT", "ACGT"))

    def test_one_mismatch(self) -> None:
        """3 matches and 1 mismatch = 2"""
        self.assertEqual(align("ACGT", "AGGT"), (2, "ACGT", "AGGT"))

    def test_one_gap(self) -> None:
        """3 matches and 1 gap = 1"""
        self.assertEqual(align("ACGT", "AGT"), (1, "ACGT", "A-GT"))

    def test_empty(self) -> None:
        """Against an empty string every letter is a gap"""
        self.assertEqual(align("", "ACG"), (-6, "---", "ACG"))
        self.assertEqual(align("", ""), (0, "", ""))

    def test_grid_edges_are_gaps(self) -> None:
        """The first row and column go down by one gap each"""
        grid = score_grid("AC", "GTA")
        self.assertEqual(grid[0], [0, -2, -4, -6])
        self.assertEqual([row[0] for row in grid], [0, -2, -4])

    def test_alignment_keeps_every_letter(self) -> None:
        """Taking the gaps back out gives the original strings"""
        a, b = "TGGCGACAACCGTAGCGG", "TGGCCACCACGATAGCAG"
        _, aligned_a, aligned_b = align(a, b)
        self.assertEqual(len(aligned_a), len(aligned_b))
        self.assertEqual(aligned_a.replace("-", ""), a)
        self.assertEqual(aligned_b.replace("-", ""), b)

    def test_match_line(self) -> None:
        """| under matching letters, a space everywhere else"""
        self.assertEqual(match_line("AC-T", "AGGT"), "|  |")


if __name__ == "__main__":
    unittest.main()
