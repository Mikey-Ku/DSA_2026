"""Times conventional vs Strassen multiplication, then sweeps the hybrid threshold
"""

import random
import time
from collections.abc import Callable

from matrix import Matrix, from_rows

SIZES = [16, 32, 64, 128, 256]
SWEEP_N = 256
THRESHOLDS = [2, 4, 8, 16, 32, 64, 128, 256]
HYBRID_THRESHOLD = 64
TRIALS = 3

def random_matrix(n: int, rng: random.Random) -> Matrix:
    """Makes an n x n matrix of random values between -10 and 10"""
    rows: list[list[float]] = []
    for _ in range(n):
        row: list[float] = []
        for _ in range(n):
            row.append(rng.uniform(-10, 10))
        rows.append(row)
    return from_rows(rows)


def best_time(run: Callable[[], object]) -> float:
    """Runs 3 times and returns the fastest time in seconds"""
    best = float("inf")
    for _ in range(TRIALS):
        start = time.perf_counter()
        run()
        best = min(best, time.perf_counter() - start)
    return best


def main() -> None:
    """Prints the conventional vs Strassen times, then the threshold sweep"""
    rng = random.Random(0)

    print("n, conventional, pure strassen, hybrid")
    for n in SIZES:
        a = random_matrix(n, rng)
        b = random_matrix(n, rng)
        conventional = best_time(lambda: a.multiply(b))
        pure = best_time(lambda: a.strassen_multiply(b, threshold=1))
        hybrid = best_time(lambda: a.strassen_multiply(b, threshold=HYBRID_THRESHOLD))
        print(n, round(conventional, 4), round(pure, 4), round(hybrid, 4))

    print()
    print("threshold, time at n =", SWEEP_N)
    a = random_matrix(SWEEP_N, rng)
    b = random_matrix(SWEEP_N, rng)
    for threshold in THRESHOLDS:
        seconds = best_time(lambda: a.strassen_multiply(b, threshold=threshold))
        print(threshold, round(seconds, 4))


if __name__ == "__main__":
    main()
