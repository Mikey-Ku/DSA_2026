"""Insertion sort."""

def insertion_sort(items: list[int]) -> None:
    """Sorts a list in place by sliding each element left into its spot.

    Args:
        items: The list to sort.
    """
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and current < items[j]:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = current
