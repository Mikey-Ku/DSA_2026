"""A doubly linked list that can store any type of value."""


class Node[T]:
    """One node in the list. It holds a value and links to the nodes on either side."""

    def __init__(self, data: T) -> None:
        """Creates a node that is not linked to any other node yet.

        Args:
            data: The value this node holds.
        """
        self.data = data
        self.prev: Node[T] | None = None
        self.next: Node[T] | None = None


class DoublyLinkedList[T]:
    """A linked list where every node links to both of its neighbors.

    The list keeps track of its first node (the head) and its last node (the tail),
    so adding or removing a value at either end takes O(1) time.
    """

    def __init__(self) -> None:
        """Creates an empty list."""
        self.head: Node[T] | None = None
        self.tail: Node[T] | None = None

    def push_front(self, data: T) -> None:
        """Adds a value to the front of the list in O(1) time.

        Args:
            data: The value to add.
        """
        node = Node(data)
        if self.head is None:
            # The list was empty, so the new node is both the first and last node.
            self.head = node
            self.tail = node
        else:
            # Link the new node and the old head to each other, then move head.
            node.next = self.head
            self.head.prev = node
            self.head = node

    def push_back(self, data: T) -> None:
        """Adds a value to the back of the list in O(1) time.

        Args:
            data: The value to add.
        """
        node = Node(data)
        if self.tail is None:
            # The list was empty, so the new node is both the first and last node.
            self.head = node
            self.tail = node
        else:
            # Link the old tail and the new node to each other, then move tail.
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def pop_front(self) -> T | None:
        """Removes the front value in O(1) time.

        Returns:
            The value that was at the front, or None if the list is empty.
        """
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        if self.head is None:
            # That was the only node, so the tail has to be cleared as well.
            self.tail = None
        else:
            # Cut the new head's link back to the removed node.
            self.head.prev = None
        return node.data

    def pop_back(self) -> T | None:
        """Removes the back value in O(1) time.

        Returns:
            The value that was at the back, or None if the list is empty.
        """
        if self.tail is None:
            return None
        node = self.tail
        self.tail = node.prev
        if self.tail is None:
            # That was the only node, so the head has to be cleared as well.
            self.head = None
        else:
            # Cut the new tail's link forward to the removed node.
            self.tail.next = None
        return node.data

    def peek_front(self) -> T | None:
        """Looks at the front value without removing it, in O(1) time.

        Returns:
            The value at the front, or None if the list is empty.
        """
        if self.head is None:
            return None
        return self.head.data

    def peek_back(self) -> T | None:
        """Looks at the back value without removing it, in O(1) time.

        Returns:
            The value at the back, or None if the list is empty.
        """
        if self.tail is None:
            return None
        return self.tail.data

    def is_empty(self) -> bool:
        """Checks whether the list has any values, in O(1) time.

        Returns:
            True if the list is empty, False otherwise.
        """
        return self.head is None
