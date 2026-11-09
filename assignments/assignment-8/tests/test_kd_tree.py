"""Tests for KDTree, quickselect and brute force search"""

import random
import unittest

from brute_force import brute_force_nearest
from kd_tree import KDTree, Leaf, Node, Point, Split, quickselect, split_on_median, squared_distance


class SquaredDistanceTest(unittest.TestCase):
    """Checks the distance helper"""

    def test_by_hand(self) -> None:
        """[0, 0] to [3, 4] is 5, so 25 squared"""
        self.assertEqual(squared_distance([0, 0], [3, 4]), 25)

    def test_same_point(self) -> None:
        """A point is distance 0 from itself"""
        self.assertEqual(squared_distance([1, 2, 3], [1, 2, 3]), 0)


class QuickselectTest(unittest.TestCase):
    """Checks that quickselect puts the right value in the target spot"""

    def test_finds_every_rank(self) -> None:
        """Every target index gets the value sorting would put there"""
        values = [[float(v)] for v in [7, 2, 9, 4, 4, 1, 8, 3, 6, 5]]
        for target in range(len(values)):
            points = list(values)
            quickselect(points, 0, len(points), target, 0)
            self.assertEqual(points[target], sorted(values)[target])

    def test_partitions_around_target(self) -> None:
        """Everything before the target is <= it and everything after is >="""
        points = [[random.random()] for _ in range(101)]
        quickselect(points, 0, len(points), 50, 0)
        median = points[50][0]
        self.assertTrue(all(p[0] <= median for p in points[:50]))
        self.assertTrue(all(p[0] >= median for p in points[51:]))

    def test_only_touches_the_range(self) -> None:
        """Points outside lo:hi stay where they are"""
        points = [[float(v)] for v in [9, 8, 7, 6, 5, 4, 3, 2, 1]]
        quickselect(points, 3, 7, 4, 0)
        self.assertEqual(points[:3], [[9.0], [8.0], [7.0]])
        self.assertEqual(points[7:], [[2.0], [1.0]])
        self.assertEqual(points[4], [4.0])


class SplitOnMedianTest(unittest.TestCase):
    """Checks the median split used to build the tree"""

    def test_less_than_goes_left(self) -> None:
        """Values < the median come first, values >= it come after"""
        points = [[float(v)] for v in [5, 1, 4, 4, 2, 4, 3]]
        median, split = split_on_median(points, 0, len(points), 0)
        self.assertEqual(median, 4)
        self.assertEqual(sorted(points[:split]), [[1.0], [2.0], [3.0]])
        self.assertTrue(all(p[0] >= 4 for p in points[split:]))


class KDTreeTest(unittest.TestCase):
    """Checks the tree's shape, then nearest neighbor against brute force"""

    def test_eight_point_example(self) -> None:
        """8 points worked out by hand split at x = 3, then y = 2 and y = 4"""
        tree = KDTree([[1, 5], [-1, 2], [4, 4], [2, 0], [-3, -3], [9, 1], [4, 1], [3, 8]])
        root = tree.root
        assert isinstance(root, Split)
        self.assertEqual((root.axis, root.median), (0, 3))
        assert isinstance(root.left, Split) and isinstance(root.right, Split)
        self.assertEqual((root.left.axis, root.left.median), (1, 2))
        self.assertEqual((root.right.axis, root.right.median), (1, 4))
        self.assertEqual(sorted(collect(root.left.left)), [[-3, -3], [2, 0]])
        self.assertEqual(sorted(collect(root.left.right)), [[-1, 2], [1, 5]])
        self.assertEqual(sorted(collect(root.right.left)), [[4, 1], [9, 1]])
        self.assertEqual(sorted(collect(root.right.right)), [[3, 8], [4, 4]])

    def test_tree_is_valid(self) -> None:
        """Every point is in its own leaf, the left side is < the median and the
        right side is >= it, and the axes cycle 0, 1, 2, 0, ..."""
        points = random_points(3, 500)
        tree = KDTree(points)
        self.assertEqual(sorted(collect(tree.root)), sorted(points))
        check_node(self, tree.root, 0, 3)

    def test_tree_is_balanced(self) -> None:
        """1024 points split in half 10 times, so 10 levels of splits and then the leaves"""
        tree = KDTree(random_points(2, 1024))
        self.assertEqual(height(tree.root), 11)

    def test_does_not_change_input(self) -> None:
        """Building the tree leaves the caller's list alone"""
        points = random_points(2, 50)
        copy = list(points)
        KDTree(points)
        self.assertEqual(points, copy)

    def test_nearest_by_hand(self) -> None:
        """The classic example: [9, 2] is closest to [8, 1]"""
        tree = KDTree([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]])
        self.assertEqual(tree.nearest([9, 2]), [8, 1])

    def test_nearest_needs_other_side(self) -> None:
        """The closest point is across the root's splitting line"""
        tree = KDTree([[0, 0], [4.9, 0], [5, 10], [6, 100], [10, 10]])
        self.assertEqual(tree.nearest([5.1, 0]), [4.9, 0])

    def test_query_is_a_point(self) -> None:
        """Searching for a point in the tree finds that point"""
        points = random_points(4, 200)
        tree = KDTree(points)
        for point in points:
            self.assertEqual(tree.nearest(point), point)

    def test_identical_points(self) -> None:
        """Copies of the same point can't be split, so they stop at one leaf"""
        tree = KDTree([[1.0, 1.0] for _ in range(5)] + [[3.0, 3.0]])
        self.assertEqual(tree.nearest([0, 0]), [1, 1])
        self.assertEqual(tree.nearest([4, 4]), [3, 3])

    def test_single_point(self) -> None:
        """A one point tree always returns that point"""
        self.assertEqual(KDTree([[1, 1]]).nearest([50, -3]), [1, 1])

    def test_duplicates(self) -> None:
        """Lots of repeated values on an axis still work"""
        points: list[Point] = [[float(i % 3), float(i % 5)] for i in range(60)]
        tree = KDTree(points)
        for query in random_points(2, 100):
            query = [query[0] * 3, query[1] * 5]
            self.assertEqual(squared_distance(query, tree.nearest(query)),
                             squared_distance(query, brute_force_nearest(points, query)))

    def test_matches_brute_force(self) -> None:
        """Random data in many dimensions gives the same answer as brute force"""
        for k in [1, 2, 3, 5, 10]:
            points = random_points(k, 300)
            tree = KDTree(points)
            for query in random_points(k, 100):
                self.assertEqual(tree.nearest(query), brute_force_nearest(points, query), f"k = {k}")


class BruteForceTest(unittest.TestCase):
    """Checks the brute force search on its own"""

    def test_by_hand(self) -> None:
        """[9, 2] is closest to [8, 1]"""
        points: list[Point] = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]
        self.assertEqual(brute_force_nearest(points, [9, 2]), [8, 1])


def random_points(k: int, n: int) -> list[Point]:
    """n random k-dimensional points between 0 and 1"""
    return [[random.random() for _ in range(k)] for _ in range(n)]


def collect(node: Node) -> list[Point]:
    """Every point in the subtree"""
    if isinstance(node, Leaf):
        return [node.point]
    return collect(node.left) + collect(node.right)


def height(node: Node) -> int:
    """Number of levels in the subtree, counting the leaves"""
    if isinstance(node, Leaf):
        return 1
    return 1 + max(height(node.left), height(node.right))


def check_node(test: unittest.TestCase, node: Node, axis: int, k: int) -> None:
    """Checks the axis and the split for node and everything under it"""
    if isinstance(node, Leaf):
        return
    test.assertEqual(node.axis, axis)
    test.assertTrue(all(p[node.axis] < node.median for p in collect(node.left)))
    test.assertTrue(all(p[node.axis] >= node.median for p in collect(node.right)))
    check_node(test, node.left, (axis + 1) % k, k)
    check_node(test, node.right, (axis + 1) % k, k)


if __name__ == "__main__":
    unittest.main()
