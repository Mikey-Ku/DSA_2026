"""Times each sorting algorithm on random lists of different sizes.

Run from the assignment-4 folder with: python3 benchmark.py
"""

import random
import time

from sorting_algorithms.insertion_sort import insertion_sort
from sorting_algorithms.merge_sort import merge_sort
from sorting_algorithms.quick_sort import quick_sort
from sorting_algorithms.selection_sort import selection_sort

SIZES = [10, 100, 1000, 10000, 100000]
TRIALS = 5
NAMES = ["Insertion sort", "Selection sort", "Merge sort", "Quick sort"]


def run_sorts(items: list[int]) -> list[float]:
    """Times every sort on its own copy of the same list.

    Args:
        items: The list to sort

    Returns:
        How long each sort took in seconds
    """
    times = []

    copy = list(items)
    start = time.perf_counter()
    insertion_sort(copy)
    times.append(time.perf_counter() - start)

    copy = list(items)
    start = time.perf_counter()
    selection_sort(copy)
    times.append(time.perf_counter() - start)

    copy = list(items)
    start = time.perf_counter()
    merge_sort(copy)
    times.append(time.perf_counter() - start)

    copy = list(items)
    start = time.perf_counter()
    quick_sort(copy)
    times.append(time.perf_counter() - start)

    return times


def main() -> None:
    """Times every sort TRIALS times at each size and prints the average."""
    for size in SIZES:
        totals = [0.0, 0.0, 0.0, 0.0]
        for _ in range(TRIALS):
            items = [random.randint(0, 999) for _ in range(size)]
            times = run_sorts(items)
            for i in range(len(times)):
                totals[i] += times[i]

        print(f"{size:,} items (average of {TRIALS} runs):")
        for i in range(len(NAMES)):
            print(f"  {NAMES[i]}: {totals[i] / TRIALS:.6f}s", flush=True)
        print()


if __name__ == "__main__":
    main()
