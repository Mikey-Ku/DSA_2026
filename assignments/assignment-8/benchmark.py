"""Times the K-D tree against brute force nearest neighbor search"""

import random
import time

from brute_force import brute_force_nearest
from kd_tree import KDTree, Point

DIMENSIONS = [1, 2, 3, 5, 10, 20]
NUM_POINTS = [10, 100, 1000, 10000, 100000]
NUM_QUERIES = 1000


def random_points(k: int, n: int, rng: random.Random) -> list[Point]:
    """n random k-dimensional points with every coordinate between 0 and 1"""
    points: list[Point] = []
    for _ in range(n):
        points.append([rng.random() for _ in range(k)])
    return points


def run_experiment(k: int, num_points: int) -> tuple[float, float, float]:
    """Benchmark KDTree against brute force nearest neighbor.

    1000 test points are matched against num_points training points, all
    k-dimensional. Returns (time to build the tree, time to query the tree with
    the 1000 points, time to answer the same 1000 queries by brute force), in
    seconds.
    """
    rng = random.Random(k * 100000 + num_points)
    training = random_points(k, num_points, rng)
    queries = random_points(k, NUM_QUERIES, rng)

    start = time.perf_counter()
    tree = KDTree(training)
    build_time = time.perf_counter() - start

    start = time.perf_counter()
    tree_answers = [tree.nearest(query) for query in queries]
    query_time = time.perf_counter() - start

    start = time.perf_counter()
    brute_answers = [brute_force_nearest(training, query) for query in queries]
    brute_time = time.perf_counter() - start

    return build_time, query_time, brute_time


def main() -> None:
    """Runs every combination of k and number of points"""
    print("k, points, build, tree query, brute force, speedup")
    for k in DIMENSIONS:
        for num_points in NUM_POINTS:
            build, query, brute = run_experiment(k, num_points)
            speedup = brute / (build + query)
            print(k, num_points, round(build, 4), round(query, 4), round(brute, 4), round(speedup, 1))


if __name__ == "__main__":
    main()
