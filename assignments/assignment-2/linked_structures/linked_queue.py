"""A queue that stores its values in a doubly linked list."""

from linked_structures.linked_list import DoublyLinkedList


class LinkedQueue[T]:
    """A first-in, first-out queue that adds to the back of a linked list and removes from the front.

    Every operation takes O(1) time because the list tracks both of its ends.
    """

    def __init__(self) -> None:
        """Creates an empty queue."""
        self.values: DoublyLinkedList[T] = DoublyLinkedList()

    def add(self, data: T) -> None:
        """Adds a value to the back of the queue.

        Args:
            data: The value to add.
        """
        self.values.push_back(data)

    def remove(self) -> T | None:
        """Removes the front value, which is the oldest one in the queue.

        Returns:
            The value that was at the front, or None if the queue is empty.
        """
        return self.values.pop_front()

    def peek(self) -> T | None:
        """Looks at the front value without removing it.

        Returns:
            The value at the front, or None if the queue is empty.
        """
        return self.values.peek_front()

    def is_empty(self) -> bool:
        """Checks whether the queue has any values.

        Returns:
            True if the queue is empty, False otherwise.
        """
        return self.values.is_empty()
