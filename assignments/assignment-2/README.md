# Assignment 2: Linked Data Structures

Michael Ku

Data Structures and Algorithms, Fall 2026

## Part 1: Doubly Linked List

`DoublyLinkedList` is in `linked_structures/linked_list.py`. It keeps track of
both its first and last nodes, so every operation takes O(1) time. Tests are in
`tests/test_linked_list.py`.

## Part 2: Stack and Queue

- `LinkedStack` (`linked_structures/linked_stack.py`) uses the front of the
  linked list as the top of the stack. Tests are in `tests/test_linked_stack.py`.
- `LinkedQueue` (`linked_structures/linked_queue.py`) adds to the back of the
  linked list and removes from the front. Tests are in `tests/test_linked_queue.py`.

## Part 3: Practice Problems

All three are in `linked_structures/practice.py`.

Note: I only wrote tests for Exercise 4, not for Exercises 3 and 5.

### Exercise 3: Reversing a stack

Pop every value into a queue, then move every value from the queue back onto the
stack. The old top leaves the queue first, so it ends up on the bottom.

### Exercise 4: Valid parentheses

Push each opening bracket onto a stack. For each closing bracket, pop the stack.
If the stack was empty or the popped bracket is a different kind, the string is
not valid. At the end, the string is valid only if the stack is empty.

Tests are in `tests/test_practice.py`: a table of strings and their expected
answers.

### Exercise 5: Copying a stack

1. Pop every value from the stack into the queue.
2. Move every value from the queue back onto the stack. The stack is now reversed.
3. Pop every value into the queue again. The bottom value is now at the front.
4. Remove each value from the queue and push it onto both the original stack and
   the new stack.

Both stacks end up with the original values in the original order.
