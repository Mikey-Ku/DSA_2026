"""Tests for every function of LinkedQueue."""

import unittest

from linked_structures.linked_queue import LinkedQueue


class LinkedQueueTest(unittest.TestCase):
    """Checks each queue operation with a few small, hand-picked cases."""

    def test_new_queue_is_empty(self) -> None:
        """A new queue is empty, and peek and dequeue both give None."""
        queue = LinkedQueue[int]()
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.peek())
        self.assertIsNone(queue.dequeue())

    def test_enqueue(self) -> None:
        """Enqueuing makes the queue non-empty and the first value stays at the front."""
        queue = LinkedQueue[int]()
        queue.enqueue(1)
        queue.enqueue(2)
        self.assertFalse(queue.is_empty())
        self.assertEqual(queue.peek(), 1)

    def test_dequeue_is_first_in_first_out(self) -> None:
        """Values come off in the same order they were added."""
        queue = LinkedQueue[int]()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.dequeue(), 3)
        self.assertTrue(queue.is_empty())

    def test_peek_does_not_remove(self) -> None:
        """Peeking twice gives the same front value and leaves the queue unchanged."""
        queue = LinkedQueue[int]()
        queue.enqueue(1)
        queue.enqueue(2)
        self.assertEqual(queue.peek(), 1)
        self.assertEqual(queue.peek(), 1)
        self.assertEqual(queue.dequeue(), 1)


if __name__ == "__main__":
    unittest.main()
