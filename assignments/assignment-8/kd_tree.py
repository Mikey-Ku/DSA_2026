"""K-D tree for nearest neighbor search.

Building: split the points at the median of one dimension (less than goes
left, greater than or equal goes right), then split each half on the next
dimension, until every point is in its own leaf.

Searching: walk down to the query's leaf like a binary search tree, then on the
way back up only check the other side of a split if it could be closer.
"""

import random

Point = list[float]

class Leaf:
    """Bottom of the tree, holds one point"""

    def __init__(self, point: Point) -> None:
        self.point = point

class Split:
    """Splits on one axis: < median goes left, >= median goes right"""

    def __init__(self, axis: int, median: float, left: "Node", right: "Node") -> None:
        self.axis = axis
        self.median = median
        self.left = left
        self.right = right

Node = Leaf | Split

class KDTree:
    """A balanced K-D tree built from a list of k-dimensional points"""

    def __init__(self, points: list[Point]) -> None:
        self.k = len(points[0])
        self.root = self.build(list(points), 0, len(points), 0)

    def build(self, points: list[Point], lo: int, hi: int, axis: int) -> Node:
        """Splits points[lo:hi] at the median of axis and builds each half"""
        if hi - lo == 1:
            return Leaf(points[lo])

        for i in range(self.k):
            split_axis = (axis + i) % self.k
            median, split = split_on_median(points, lo, hi, split_axis)
            if split > lo:
                next_axis = (split_axis + 1) % self.k
                left = self.build(points, lo, split, next_axis)
                right = self.build(points, split, hi, next_axis)
                return Split(split_axis, median, left, right)

        return Leaf(points[lo])

    def nearest(self, query: Point) -> Point:
        """The point in the tree closest to query"""
        best = [None, float("inf")]
        self.search(self.root, query, best)
        return best[0]

    def search(self, node: Node, query: Point, best: list) -> None:
        """Updates best = [point, squared distance] with anything closer under node"""
        if isinstance(node, Leaf):
            dist = squared_distance(query, node.point)
            if dist < best[1]:
                best[0] = node.point
                best[1] = dist
            return

        diff = query[node.axis] - node.median
        if diff < 0:
            near, far = node.left, node.right
        else:
            near, far = node.right, node.left
        self.search(near, query, best)

        if diff * diff < best[1]:
            self.search(far, query, best)

def squared_distance(a: Point, b: Point) -> float:
    """Euclidean distance squared (no square root, same ordering)"""
    total = 0.0
    for i in range(len(a)):
        total += (a[i] - b[i]) * (a[i] - b[i])
    return total

def split_on_median(points: list[Point], lo: int, hi: int, axis: int) -> tuple[float, int]:
    """Moves points < the median to the front. Returns the median and where >= starts"""
    mid = (lo + hi) // 2
    quickselect(points, lo, hi, mid, axis)
    median = points[mid][axis]

    split = move_less_to_front(points, lo, mid, axis, median)

    if split == lo:
        bigger = [p[axis] for p in points[mid:hi] if p[axis] > median]
        if bigger:
            median = min(bigger)
            split = move_less_to_front(points, lo, hi, axis, median)
    return median, split

def move_less_to_front(points: list[Point], lo: int, hi: int, axis: int, value: float) -> int:
    """Moves points in points[lo:hi] with axis < value to the front, returns where they end"""
    split = lo
    for i in range(lo, hi):
        if points[i][axis] < value:
            points[i], points[split] = points[split], points[i]
            split += 1
    return split

def quickselect(points: list[Point], lo: int, hi: int, target: int, axis: int) -> None:
    """Puts the target-th smallest point on axis at index target. Average Θ(n)"""
    hi -= 1
    while lo < hi:
        pivot = partition(points, lo, hi, axis)
        if target == pivot:
            return
        if target < pivot:
            hi = pivot - 1
        else:
            lo = pivot + 1

def partition(points: list[Point], lo: int, hi: int, axis: int) -> int:
    """Splits points[lo:hi + 1] around a random pivot, returns the pivot's index"""
    pick = random.randint(lo, hi)
    points[pick], points[hi] = points[hi], points[pick]
    pivot_value = points[hi][axis]

    store = lo
    for i in range(lo, hi):
        if points[i][axis] < pivot_value:
            points[i], points[store] = points[store], points[i]
            store += 1

    points[store], points[hi] = points[hi], points[store]
    return store
