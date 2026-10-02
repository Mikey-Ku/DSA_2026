"""Quick sort."""


def quick_sort(items: list[int], start: int = 0, end: int | None = None) -> None:
    """Sorts a list in place by partitioning around a pivot and sorting each side.

    Args:
        items: The list to sort.
        start: The first index of the part to sort.
        end: The last index of the part to sort. Defaults to the end of the list.
    """
    if end is None:
        end = len(items) - 1
    if start >= end:
        return

    pivot_index = partition(items, start, end)
    quick_sort(items, start, pivot_index - 1)
    quick_sort(items, pivot_index + 1, end)


def partition(items: list[int], start: int, end: int) -> int:
    """Moves smaller elements left of the pivot and bigger ones right of it.

    The first element of the range is used as the pivot.

    Args:
        items: The list to partition.
        start: The first index of the range.
        end: The last index of the range.

    Returns:
        The index the pivot ends up at.
    """
    pivot = items[start]
    low = start + 1
    high = end

    while True:
        while low <= high and items[high] >= pivot:
            high = high - 1

        while low <= high and items[low] <= pivot:
            low = low + 1

        if low <= high:
            items[low], items[high] = items[high], items[low]
        else:
            break

    items[start], items[high] = items[high], items[start]

    return high
