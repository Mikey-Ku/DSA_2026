"""Merge sort."""

def merge_sort(items: list[int]) -> None:
    """Sorts a list in place by sorting each half and merging them back together.

    Args:
        items: The list to sort.
    """
    if len(items) > 1:
        middle = len(items) // 2
        left = items[:middle]
        right = items[middle:]

        merge_sort(left)
        merge_sort(right)

        i = 0  # next index in left
        j = 0  # next index in right
        k = 0  # next index in items to fill

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                items[k] = left[i]
                i += 1
            else:
                items[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            items[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            items[k] = right[j]
            j += 1
            k += 1
