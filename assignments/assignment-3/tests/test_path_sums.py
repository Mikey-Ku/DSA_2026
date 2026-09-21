"""Tests for the Project Euler problem 81 solution."""

import unittest

from graphs.path_sums import smallest_path, smallest_sum

EXAMPLE_MATRIX = [
    [131, 673, 234, 103, 18],
    [201, 96, 342, 965, 150],
    [630, 803, 746, 422, 111],
    [537, 699, 497, 121, 956],
    [805, 732, 524, 37, 331],
]


class PathSumsTest(unittest.TestCase):
    """Checks problem 81 on the example matrix and on small matrices by hand."""

    def test_finds_the_answer_from_the_example(self) -> None:
        """The sum and path match the ones on the Project Euler problem page."""
        self.assertEqual(smallest_sum(EXAMPLE_MATRIX), 2427)
        self.assertEqual(
            [EXAMPLE_MATRIX[row][col] for row, col in smallest_path(EXAMPLE_MATRIX)],
            [131, 201, 96, 342, 746, 422, 121, 37, 331],
        )

    def test_a_matrix_with_one_cell_has_a_path_of_just_that_cell(self) -> None:
        """With only one cell, it is both the start and the end."""
        self.assertEqual(smallest_path([[7]]), [(0, 0)])
        self.assertEqual(smallest_sum([[7]]), 7)

    def test_a_single_row_or_column_uses_every_cell(self) -> None:
        """With one row there is only right to move, and with one column only down."""
        self.assertEqual(smallest_path([[4, 8, 2]]), [(0, 0), (0, 1), (0, 2)])
        self.assertEqual(smallest_path([[4], [8], [2]]), [(0, 0), (1, 0), (2, 0)])

    def test_a_two_by_two_matrix_picks_the_cheaper_way_around(self) -> None:
        """Both corners are on every path, so the choice is which middle cell to use."""
        matrix = [[1, 9], [2, 1]]
        self.assertEqual(smallest_path(matrix), [(0, 0), (1, 0), (1, 1)])
        self.assertEqual(smallest_sum(matrix), 4)

    def test_goes_around_large_numbers(self) -> None:
        """Going down the cheap first column beats cutting across the 9s."""
        matrix = [[1, 9, 9], [1, 9, 9], [1, 1, 1]]
        self.assertEqual(smallest_path(matrix), [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])
        self.assertEqual(smallest_sum(matrix), 5)

    def test_a_path_of_zeros_costs_nothing(self) -> None:
        """Cells that cost nothing are allowed, and the cheapest path uses them."""
        matrix = [[0, 5, 5], [0, 0, 0], [5, 5, 0]]
        self.assertEqual(smallest_path(matrix), [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)])
        self.assertEqual(smallest_sum(matrix), 0)


if __name__ == "__main__":
    unittest.main()
