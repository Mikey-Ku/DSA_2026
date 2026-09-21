"""A binary min heap where the priority of an element can be changed."""

import math
from collections.abc import Hashable
from typing import NamedTuple


class _Entry[T](NamedTuple):
    """An element in the heap and its priority."""

    element: T
    priority: float


class MinHeap[T: Hashable]:
    """Representation of a min heap.

    using the scheme in https://en.wikipedia.org/wiki/Heap_(data_structure)
    """

    def __init__(self) -> None:
        self._entries: list[_Entry[T]] = []
        self._index_of: dict[T, int] = {}

    def __len__(self) -> int:
        """Returns the number of elements in the heap."""
        return len(self._entries)

    def __contains__(self, element: object) -> bool:
        """Returns True if the element is in the heap, False otherwise."""
        return element in self._index_of

    def is_empty(self) -> bool:
        """Returns True if the heap is empty, False otherwise."""
        return not self._entries

    def insert(self, element: T, priority: float) -> None:
        """Inserts element into the heap with the given priority.

        Raises a ValueError if the element is already in the heap.
        """
        if element in self._index_of:
            raise ValueError(f"{element!r} is already in the heap.")
        _check_priority(element, priority)
        self._entries.append(_Entry(element, priority))
        self._index_of[element] = len(self._entries) - 1
        self._sift_up(len(self._entries) - 1)

    def peek(self) -> T | None:
        """Returns the minimum element without removing it (or None if the heap is empty)."""
        if not self._entries:
            return None
        return self._entries[0].element

    def remove_min(self) -> T | None:
        """Removes and returns the minimum element (or None if the heap is empty)."""
        if not self._entries:
            return None
        minimum = self._entries[0].element
        self._swap(0, len(self._entries) - 1)
        self._entries.pop()
        del self._index_of[minimum]
        if self._entries:
            self._sift_down(0)
        return minimum

    def change_priority(self, element: T, priority: float) -> None:
        """Changes the priority of an element.

        Raises a ValueError if the element is not in the heap.
        """
        index = self._index_of.get(element)
        if index is None:
            raise ValueError(f"{element!r} is not in the heap.")
        _check_priority(element, priority)
        old_priority = self._entries[index].priority
        self._entries[index] = _Entry(element, priority)
        if priority < old_priority:
            self._sift_up(index)
        else:
            self._sift_down(index)

    def _sift_up(self, index: int) -> None:
        """Moves the element at index up if needed."""
        while index > 0:
            parent = (index - 1) // 2
            if self._entries[parent].priority <= self._entries[index].priority:
                return
            self._swap(index, parent)
            index = parent

    def _sift_down(self, index: int) -> None:
        """Moves the element at index down if needed."""
        entries = self._entries
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            if left < len(entries) and entries[left].priority < entries[smallest].priority:
                smallest = left
            if right < len(entries) and entries[right].priority < entries[smallest].priority:
                smallest = right
            if smallest == index:
                return
            self._swap(index, smallest)
            index = smallest

    def _swap(self, first: int, second: int) -> None:
        """Swaps two entries in the list."""
        entries = self._entries
        entries[first], entries[second] = entries[second], entries[first]
        # update the index map so we can still find things
        self._index_of[entries[first].element] = first
        self._index_of[entries[second].element] = second


def _check_priority(element: object, priority: float) -> None:
    """Raises a ValueError if the priority is NaN."""
    if math.isnan(priority):
        raise ValueError(f"The priority of {element!r} must be a number.")
