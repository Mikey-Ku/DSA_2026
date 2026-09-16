"""Tests for every function of LinkedQueue."""

import unittest

from linked_structures.linked_queue import LinkedQueue


class LinkedQueueTest(unittest.TestCase):
    """Checks each queue operation with a few small, hand-picked cases."""

    def test_new_queue_is_empty(self) -> None:
        """A new queue is empty, and peek and remove both give None."""
        queue = LinkedQueue[int]()
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.peek())
        self.assertIsNone(queue.remove())

    def test_add(self) -> None:
        """Adding makes the queue non-empty and the first value stays at the front."""
        queue = LinkedQueue[int]()
        queue.add(1)
        queue.add(2)
        self.assertFalse(queue.is_empty())
        self.assertEqual(queue.peek(), 1)

    def test_remove_is_first_in_first_out(self) -> None:
        """Values come off in the same order they were added."""
        queue = LinkedQueue[int]()
        queue.add(1)
        queue.add(2)
        queue.add(3)
        self.assertEqual(queue.remove(), 1)
        self.assertEqual(queue.remove(), 2)
        self.assertEqual(queue.remove(), 3)
        self.assertTrue(queue.is_empty())

    def test_peek_does_not_remove(self) -> None:
        """Peeking twice gives the same front value and leaves the queue unchanged."""
        queue = LinkedQueue[int]()
        queue.add(1)
        queue.add(2)
        self.assertEqual(queue.peek(), 1)
        self.assertEqual(queue.peek(), 1)
        self.assertEqual(queue.remove(), 1)


if __name__ == "__main__":
    unittest.main()
