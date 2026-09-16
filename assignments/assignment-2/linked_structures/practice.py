"""Practice problems solved with the linked stack and queue."""

from linked_structures.linked_queue import LinkedQueue
from linked_structures.linked_stack import LinkedStack


# Exercise 3
def reverse_stack[T](stack: LinkedStack[T]) -> None:
    """Reverses a stack in place, so the old top ends up on the bottom.

    Args:
        stack: The stack to reverse. It is changed directly.
    """
    queue: LinkedQueue[T] = LinkedQueue()

    # Pop every value into the queue. The old top goes in first.
    while not stack.is_empty():
        value = stack.pop()
        if value is not None:
            queue.add(value)

    # Push every value back. The old top comes out first, so it lands on the bottom.
    while not queue.is_empty():
        value = queue.remove()
        if value is not None:
            stack.push(value)


# Exercise 4
def is_valid_parentheses(text: str) -> bool:
    """Checks that every bracket in the text is closed by the same kind, in the right order.

    Characters other than (), [], and {} are ignored.

    Args:
        text: The string to check.

    Returns:
        True if the brackets are balanced and properly nested, False otherwise.
    """
    # Maps each closing bracket to the opening bracket it must match.
    bracket_pairings = {")": "(", "]": "[", "}": "{"}

    open_brackets: LinkedStack[str] = LinkedStack()
    for char in text:
        if char in "([{":
            open_brackets.push(char)
        elif char in bracket_pairings:
            # The most recent unclosed bracket must be the matching kind. Popping an
            # empty stack gives None, which never matches, so a stray closer fails too.
            last_open = open_brackets.pop()
            if last_open != bracket_pairings[char]:
                return False

    # Anything still on the stack was opened but never closed.
    return open_brackets.is_empty()


# Exercise 5
def copy_stack[T](stack: LinkedStack[T]) -> LinkedStack[T]:
    """Makes a copy of a stack using only one queue as extra storage.

    The original stack ends up with the same values in the same order it started with.

    Args:
        stack: The stack to copy.

    Returns:
        A new stack with the same values in the same order.
    """
    queue: LinkedQueue[T] = LinkedQueue()

    # Pop every value into the queue. The old top goes in first.
    while not stack.is_empty():
        value = stack.pop()
        if value is not None:
            queue.add(value)

    # Push it all back. The stack is now upside down.
    while not queue.is_empty():
        value = queue.remove()
        if value is not None:
            stack.push(value)

    # Pop it into the queue again. Now the original bottom value is at the front.
    while not stack.is_empty():
        value = stack.pop()
        if value is not None:
            queue.add(value)

    # Rebuild the original stack and the copy at the same time, bottom value first.
    copy: LinkedStack[T] = LinkedStack()
    while not queue.is_empty():
        value = queue.remove()
        if value is not None:
            stack.push(value)
            copy.push(value)
    return copy
