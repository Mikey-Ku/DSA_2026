"""Selection sort."""


def selection_sort(items: list[int]) -> None:
    """Sorts a list in place by swapping the smallest remaining element to the front.

    Args:
        items: The list to sort.
    """
    for i in range(len(items)):
        smallest = i
        for j in range(i + 1, len(items)):
            if items[smallest] > items[j]:
                smallest = j
        items[i], items[smallest] = items[smallest], items[i]
