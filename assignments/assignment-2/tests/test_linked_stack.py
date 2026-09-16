"""Tests for every function of LinkedStack."""

import unittest

from linked_structures.linked_stack import LinkedStack


class LinkedStackTest(unittest.TestCase):
    """Checks each stack operation with a few small, hand-picked cases."""

    def test_new_stack_is_empty(self) -> None:
        """A new stack is empty, and peek and pop both give None."""
        stack = LinkedStack[int]()
        self.assertTrue(stack.is_empty())
        self.assertIsNone(stack.peek())
        self.assertIsNone(stack.pop())

    def test_push(self) -> None:
        """Pushing makes the stack non-empty and puts the value on top."""
        stack = LinkedStack[int]()
        stack.push(1)
        self.assertFalse(stack.is_empty())
        self.assertEqual(stack.peek(), 1)

    def test_pop_is_last_in_first_out(self) -> None:
        """Values come off in the reverse of the order they were pushed."""
        stack = LinkedStack[int]()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)
        self.assertTrue(stack.is_empty())

    def test_peek_does_not_remove(self) -> None:
        """Peeking twice gives the same top value and leaves the stack unchanged."""
        stack = LinkedStack[int]()
        stack.push(1)
        stack.push(2)
        self.assertEqual(stack.peek(), 2)
        self.assertEqual(stack.peek(), 2)
        self.assertEqual(stack.pop(), 2)


if __name__ == "__main__":
    unittest.main()
