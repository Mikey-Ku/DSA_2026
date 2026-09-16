"""A stack that stores its values in a doubly linked list."""

from linked_structures.linked_list import DoublyLinkedList


class LinkedStack[T]:
    """A last-in, first-out stack that uses the front of a linked list as its top.

    Every operation takes O(1) time because it only touches the front of the list.
    """

    def __init__(self) -> None:
        """Creates an empty stack."""
        self.values: DoublyLinkedList[T] = DoublyLinkedList()

    def push(self, data: T) -> None:
        """Adds a value to the top of the stack.

        Args:
            data: The value to add.
        """
        self.values.push_front(data)

    def pop(self) -> T | None:
        """Removes the top value.

        Returns:
            The value that was on top, or None if the stack is empty.
        """
        return self.values.pop_front()

    def peek(self) -> T | None:
        """Looks at the top value without removing it.

        Returns:
            The value on top, or None if the stack is empty.
        """
        return self.values.peek_front()

    def is_empty(self) -> bool:
        """Checks whether the stack has any values.

        Returns:
            True if the stack is empty, False otherwise.
        """
        return self.values.is_empty()
