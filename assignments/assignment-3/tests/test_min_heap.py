"""Tests for MinHeap."""

import math
import random
import unittest
from collections.abc import Hashable

from graphs.min_heap import MinHeap


def drain[T: Hashable](heap: MinHeap[T]) -> list[T]:
    """Removes every element from a heap.

    Args:
        heap: The heap to empty.

    Returns:
        The elements in the order they came out.
    """
    removed: list[T] = []
    while (element := heap.remove_min()) is not None:
        removed.append(element)
    return removed


class MinHeapTest(unittest.TestCase):
    """Checks each heap operation, then compares the heap with a simpler version."""

    def test_new_heap_is_empty(self) -> None:
        """A new heap is empty, and peek and remove_min both give None."""
        heap: MinHeap[str] = MinHeap()
        self.assertTrue(heap.is_empty())
        self.assertEqual(len(heap), 0)
        self.assertIsNone(heap.peek())
        self.assertIsNone(heap.remove_min())

    def test_elements_come_out_from_lowest_to_highest_priority(self) -> None:
        """remove_min always gives the element with the lowest priority left."""
        heap: MinHeap[str] = MinHeap()
        heap.insert("C", 3)
        heap.insert("A", 1)
        heap.insert("D", 4)
        heap.insert("B", 2)
        self.assertEqual(len(heap), 4)
        self.assertEqual(drain(heap), ["A", "B", "C", "D"])
        self.assertTrue(heap.is_empty())

    def test_peek_does_not_remove(self) -> None:
        """Peeking twice gives the same element and leaves the heap unchanged."""
        heap: MinHeap[str] = MinHeap()
        heap.insert("B", 2)
        heap.insert("A", 1)
        self.assertEqual(heap.peek(), "A")
        self.assertEqual(heap.peek(), "A")
        self.assertEqual(len(heap), 2)

    def test_contains_only_while_in_the_heap(self) -> None:
        """An element is in the heap after it is inserted and until it is removed."""
        heap: MinHeap[str] = MinHeap()
        heap.insert("A", 1)
        self.assertIn("A", heap)
        self.assertNotIn("B", heap)
        heap.remove_min()
        self.assertNotIn("A", heap)

    def test_changing_a_priority_moves_an_element(self) -> None:
        """Lowering a priority moves an element forward, raising it moves it back.

        Setting a priority to the value it already had leaves the order alone.
        """
        heap: MinHeap[str] = MinHeap()
        for name, priority in [("A", 1), ("B", 2), ("C", 3)]:
            heap.insert(name, priority)
        heap.change_priority("C", 0.5)
        heap.change_priority("B", 2)
        heap.change_priority("A", 10)
        self.assertEqual(drain(heap), ["C", "B", "A"])

    def test_negative_and_infinite_priorities_are_allowed(self) -> None:
        """Any number works as a priority, including negative numbers and infinity."""
        heap: MinHeap[str] = MinHeap()
        heap.insert("far", math.inf)
        heap.insert("negative", -5)
        heap.insert("zero", 0)
        self.assertEqual(drain(heap), ["negative", "zero", "far"])

    def test_equal_priorities_all_come_out(self) -> None:
        """Ties can come out in any order, but every element still comes out once."""
        heap: MinHeap[str] = MinHeap()
        for name in ["A", "B", "C", "D"]:
            heap.insert(name, 1)
        heap.insert("E", 0)
        removed = drain(heap)
        self.assertEqual(removed[0], "E")
        self.assertCountEqual(removed, ["A", "B", "C", "D", "E"])

    def test_invalid_calls_fail(self) -> None:
        """An element can only be in the heap once, and NaN is not a usable priority.

        NaN is never less than, equal to, or greater than anything, so it would
        silently break every comparison the heap makes.
        """
        heap: MinHeap[str] = MinHeap()
        with self.assertRaises(ValueError):
            heap.change_priority("A", 1)
        with self.assertRaises(ValueError):
            heap.insert("A", math.nan)
        heap.insert("A", 1)
        with self.assertRaises(ValueError):
            heap.insert("A", 2)
        with self.assertRaises(ValueError):
            heap.change_priority("A", math.nan)

    def test_an_element_can_be_added_again_after_it_is_removed(self) -> None:
        """Removing the only element must also forget the index stored for it."""
        heap: MinHeap[str] = MinHeap()
        heap.insert("A", 1)
        self.assertEqual(heap.remove_min(), "A")
        heap.insert("A", 2)
        heap.insert("B", 1)
        heap.change_priority("A", 0)
        self.assertEqual(drain(heap), ["A", "B"])

    def test_random_calls_agree_with_a_dictionary(self) -> None:
        """10,000 random calls give the same results as a plain dictionary of priorities.

        Finding the minimum in a dictionary means checking every entry, which is slow
        but clearly correct.
        """
        rng = random.Random(3)
        heap: MinHeap[int] = MinHeap()
        expected: dict[int, float] = {}

        for step in range(10_000):
            action = rng.randrange(3)
            if action == 0:
                element = rng.randrange(200)
                if element not in expected:
                    priority = float(rng.randrange(50))
                    heap.insert(element, priority)
                    expected[element] = priority
            elif action == 1:
                removed = heap.remove_min()
                if not expected:
                    self.assertIsNone(removed, f"step {step}")
                elif removed is None:
                    self.fail(f"step {step}: the heap ran out of elements too soon")
                else:
                    # When priorities tie, any element with the lowest priority is correct.
                    self.assertEqual(expected[removed], min(expected.values()), f"step {step}")
                    del expected[removed]
            elif expected:
                element = rng.choice(list(expected))
                priority = float(rng.randrange(50))
                heap.change_priority(element, priority)
                expected[element] = priority
            self.assertEqual(len(heap), len(expected), f"step {step}")


if __name__ == "__main__":
    unittest.main()
