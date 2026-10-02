"""Tests for insertion, selection, merge, and quick sort."""

import random
import unittest

from sorting_algorithms.insertion_sort import insertion_sort
from sorting_algorithms.merge_sort import merge_sort
from sorting_algorithms.quick_sort import quick_sort
from sorting_algorithms.selection_sort import selection_sort


class SortingTest(unittest.TestCase):
    """Runs every sort on the same inputs and compares with Python's sorted()."""

    def check(self, items: list[int]) -> None:
        """Sorts a copy of the list with each sort and checks it matches sorted()."""
        expected = sorted(items)

        copy = list(items)
        insertion_sort(copy)
        self.assertEqual(copy, expected, "insertion_sort")

        copy = list(items)
        selection_sort(copy)
        self.assertEqual(copy, expected, "selection_sort")

        copy = list(items)
        merge_sort(copy)
        self.assertEqual(copy, expected, "merge_sort")

        copy = list(items)
        quick_sort(copy)
        self.assertEqual(copy, expected, "quick_sort")

    def test_empty(self) -> None:
        """An empty list stays empty."""
        self.check([])

    def test_one_element(self) -> None:
        """A single element is already sorted."""
        self.check([7])

    def test_two_elements(self) -> None:
        """Two elements in either order."""
        self.check([1, 2])
        self.check([2, 1])

    def test_already_sorted(self) -> None:
        """A sorted list stays the same."""
        self.check(list(range(200)))

    def test_reversed(self) -> None:
        """A backwards list gets flipped."""
        self.check(list(range(200, 0, -1)))

    def test_duplicates(self) -> None:
        """Repeated values, including a list that's all the same value."""
        self.check([3, 1, 3, 2, 1, 3, 2, 2, 1])
        self.check([5] * 100)

    def test_negatives(self) -> None:
        """Negative numbers mixed with positive ones and zero."""
        self.check([-2, 3, 0, -7, 1, 3, -5])

    def test_random(self) -> None:
        """Random lists of different lengths."""
        for length in [3, 10, 57, 256, 1000]:
            self.check([random.randint(-50, 50) for _ in range(length)])


if __name__ == "__main__":
    unittest.main()
