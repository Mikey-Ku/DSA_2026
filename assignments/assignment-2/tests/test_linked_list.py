"""Tests for every function of DoublyLinkedList."""

import unittest

from linked_structures.linked_list import DoublyLinkedList


class DoublyLinkedListTest(unittest.TestCase):
    """Checks each list operation with a few small, hand-picked cases."""

    def test_new_list_is_empty(self) -> None:
        """A new list is empty and has nothing to peek at."""
        items = DoublyLinkedList[int]()
        self.assertTrue(items.is_empty())
        self.assertIsNone(items.peek_front())
        self.assertIsNone(items.peek_back())

    def test_push_front(self) -> None:
        """Each value pushed to the front becomes the new front."""
        items = DoublyLinkedList[int]()
        items.push_front(1)
        items.push_front(2)
        self.assertFalse(items.is_empty())
        self.assertEqual(items.peek_front(), 2)
        self.assertEqual(items.peek_back(), 1)

    def test_push_back(self) -> None:
        """Each value pushed to the back becomes the new back."""
        items = DoublyLinkedList[int]()
        items.push_back(1)
        items.push_back(2)
        self.assertFalse(items.is_empty())
        self.assertEqual(items.peek_front(), 1)
        self.assertEqual(items.peek_back(), 2)

    def test_pop_front(self) -> None:
        """Values come off the front in order, then None once the list is empty."""
        items = DoublyLinkedList[int]()
        items.push_back(1)
        items.push_back(2)
        self.assertEqual(items.pop_front(), 1)
        self.assertEqual(items.pop_front(), 2)
        self.assertIsNone(items.pop_front())
        self.assertTrue(items.is_empty())

    def test_pop_back(self) -> None:
        """Values come off the back in order, then None once the list is empty."""
        items = DoublyLinkedList[int]()
        items.push_back(1)
        items.push_back(2)
        self.assertEqual(items.pop_back(), 2)
        self.assertEqual(items.pop_back(), 1)
        self.assertIsNone(items.pop_back())
        self.assertTrue(items.is_empty())

    def test_peek_does_not_remove(self) -> None:
        """Peeking twice gives the same value and leaves the list unchanged."""
        items = DoublyLinkedList[int]()
        items.push_back(1)
        items.push_back(2)
        self.assertEqual(items.peek_front(), 1)
        self.assertEqual(items.peek_front(), 1)
        self.assertEqual(items.peek_back(), 2)
        self.assertEqual(items.peek_back(), 2)

    def test_removing_only_value_clears_both_ends(self) -> None:
        """With one value, popping either end empties the whole list."""
        items = DoublyLinkedList[int]()
        items.push_front(1)
        self.assertEqual(items.pop_back(), 1)
        self.assertTrue(items.is_empty())
        self.assertIsNone(items.peek_front())
        self.assertIsNone(items.peek_back())

    def test_pop_from_both_ends(self) -> None:
        """Alternating pops check that the prev and next links stay correct."""
        items = DoublyLinkedList[int]()
        for value in [1, 2, 3, 4]:
            items.push_back(value)
        self.assertEqual(items.pop_front(), 1)
        self.assertEqual(items.pop_back(), 4)
        self.assertEqual(items.pop_front(), 2)
        self.assertEqual(items.pop_back(), 3)
        self.assertTrue(items.is_empty())


if __name__ == "__main__":
    unittest.main()
