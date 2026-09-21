
from collections.abc import Hashable

from graphs.min_heap import MinHeap


class PriorityQueue[T: Hashable]:
    """A min priority queue that keeps its elements in a MinHeap.

    The lower an element's priority value, the sooner it is removed from the queue.
    """

    def __init__(self) -> None:
        """Creates an empty queue."""
        self._heap: MinHeap[T] = MinHeap()

    def is_empty(self) -> bool:
        """Checks whether the queue is empty.

        Returns:
            True if the queue is empty, False otherwise.
        """
        return self._heap.is_empty()

    def add_with_priority(self, elem: T, priority: float) -> None:
        """Adds an element to the queue.

        Args:
            elem: The element to add.
            priority: The element's priority. Lower priorities come out first.

        Raises:
            ValueError: If elem is already in the queue.
        """
        self._heap.insert(elem, priority)

    def next(self) -> T | None:
        """Removes the next element, which is the one with the lowest priority.

        Returns:
            The next element, or None if the queue is empty.
        """
        return self._heap.remove_min()

    def adjust_priority(self, elem: T, new_priority: float) -> None:
        """Changes the priority of an element in the queue.

        Args:
            elem: The element whose priority should change.
            new_priority: The new priority.

        Raises:
            ValueError: If elem is not in the queue.
        """
        self._heap.change_priority(elem, new_priority)
