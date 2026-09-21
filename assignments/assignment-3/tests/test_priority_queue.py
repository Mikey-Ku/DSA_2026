"""Tests for PriorityQueue."""

import unittest

from graphs.priority_queue import PriorityQueue


class PriorityQueueTest(unittest.TestCase):
    """Checks the queue's methods. The heap underneath has its own tests."""

    def test_new_queue_is_empty(self) -> None:
        """A new queue is empty, and next gives None."""
        queue: PriorityQueue[str] = PriorityQueue()
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.next())

    def test_next_returns_the_lowest_priority_first(self) -> None:
        """Elements come out in order of priority, not the order they were added."""
        queue: PriorityQueue[str] = PriorityQueue()
        queue.add_with_priority("second", 2)
        queue.add_with_priority("third", 3)
        queue.add_with_priority("first", 1)
        self.assertFalse(queue.is_empty())
        self.assertEqual(queue.next(), "first")
        self.assertEqual(queue.next(), "second")
        self.assertEqual(queue.next(), "third")
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.next())

    def test_adjusting_a_priority_changes_when_an_element_comes_out(self) -> None:
        """Lowering a priority moves an element earlier, and raising it moves it later."""
        queue: PriorityQueue[str] = PriorityQueue()
        queue.add_with_priority("A", 1)
        queue.add_with_priority("B", 2)
        queue.add_with_priority("C", 3)
        queue.adjust_priority("C", 0)
        queue.adjust_priority("A", 5)
        self.assertEqual(queue.next(), "C")
        self.assertEqual(queue.next(), "B")
        self.assertEqual(queue.next(), "A")

    def test_invalid_calls_fail(self) -> None:
        """An element can only be added once, and only an element in the queue can be adjusted."""
        queue: PriorityQueue[str] = PriorityQueue()
        queue.add_with_priority("A", 1)
        with self.assertRaises(ValueError):
            queue.add_with_priority("A", 2)
        with self.assertRaises(ValueError):
            queue.adjust_priority("B", 1)


if __name__ == "__main__":
    unittest.main()
