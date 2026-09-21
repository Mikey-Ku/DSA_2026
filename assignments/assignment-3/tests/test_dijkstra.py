"""Tests for shortest_path, the Dijkstra's algorithm search."""

import math
import unittest
from collections.abc import Hashable
from itertools import pairwise

from graphs.dijkstra import shortest_path
from graphs.graph import DirectedGraph


def cost_of[V: Hashable](graph: DirectedGraph[V], path: list[V]) -> float:
    """Adds up the edge costs along a path.

    Args:
        graph: The graph the path goes through.
        path: The vertices along the path.

    Returns:
        The total cost of the path's edges.

    Raises:
        AssertionError: If the path takes a step that is not an edge.
    """
    total = 0.0
    for before, after in pairwise(path):
        edges = graph.get_edges(before)
        if after not in edges:
            raise AssertionError(f"The path steps from {before!r} to {after!r}, but there is no such edge.")
        total += edges[after]
    return total


class ShortestPathTest(unittest.TestCase):
    """Checks shortest_path on small graphs whose answers can be worked out by hand."""

    def test_prefers_a_cheaper_path_with_more_edges(self) -> None:
        """Two cheap edges beat one expensive edge."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 10)
        graph.add_edge("A", "C", 1)
        graph.add_edge("C", "B", 2)
        self.assertEqual(shortest_path(graph, "A", "B"), ["A", "C", "B"])

    def test_a_cheaper_path_found_later_replaces_the_earlier_one(self) -> None:
        """B is first reached straight from A for 10, and later through C for 2.

        B's priority has to drop to 2 at that point. Otherwise D, which the direct
        edge puts in the queue at 5, would come out before B, and the search would
        stop with A -> D instead of the cheaper A -> C -> B -> D.
        """
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 10)
        graph.add_edge("A", "C", 1)
        graph.add_edge("C", "B", 1)
        graph.add_edge("B", "D", 1)
        graph.add_edge("A", "D", 5)
        self.assertEqual(shortest_path(graph, "A", "D"), ["A", "C", "B", "D"])

    def test_finds_the_shortest_path_in_a_larger_undirected_example(self) -> None:
        """Each road can be traveled both ways, so it becomes two directed edges."""
        roads = [
            (1, 2, 7),
            (1, 3, 9),
            (1, 6, 14),
            (2, 3, 10),
            (2, 4, 15),
            (3, 4, 11),
            (3, 6, 2),
            (4, 5, 6),
            (5, 6, 9),
        ]
        graph: DirectedGraph[int] = DirectedGraph()
        for a, b, cost in roads:
            graph.add_edge(a, b, cost)
            graph.add_edge(b, a, cost)
        path = shortest_path(graph, 1, 5)
        self.assertEqual(path, [1, 3, 6, 5])
        if path is not None:
            self.assertEqual(cost_of(graph, path), 20)

    def test_the_path_from_a_vertex_to_itself_is_just_that_vertex(self) -> None:
        """Getting from a vertex to itself costs nothing and needs no edges."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 1)
        self.assertEqual(shortest_path(graph, "A", "A"), ["A"])

    def test_returns_none_when_there_is_no_path(self) -> None:
        """Separate parts of a graph, the wrong way down an edge, and missing vertices."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("C", "D", 1)
        self.assertEqual(shortest_path(graph, "A", "B"), ["A", "B"])
        self.assertIsNone(shortest_path(graph, "A", "D"))
        self.assertIsNone(shortest_path(graph, "B", "A"))
        self.assertIsNone(shortest_path(graph, "A", "Z"))
        self.assertIsNone(shortest_path(graph, "Z", "Z"))

    def test_edges_that_cost_nothing_are_allowed(self) -> None:
        """Zero-cost edges are fine, since they never make a path cheaper."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 0)
        graph.add_edge("B", "C", 0)
        graph.add_edge("A", "C", 1)
        self.assertEqual(shortest_path(graph, "A", "C"), ["A", "B", "C"])

    def test_cycles_do_not_cause_trouble(self) -> None:
        """Edges back to earlier vertices, and self loops, don't cause an endless loop."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("B", "A", 1)
        graph.add_edge("B", "B", 1)
        graph.add_edge("B", "C", 1)
        self.assertEqual(shortest_path(graph, "A", "C"), ["A", "B", "C"])

    def test_a_negative_edge_is_rejected_even_if_the_search_could_finish_without_it(self) -> None:
        """T comes out of the queue at 5, before X at 100.

        A search that only checked the edges it followed would return A -> T, and
        never notice that A -> X -> T costs -100.
        """
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "T", 5)
        graph.add_edge("A", "X", 100)
        graph.add_edge("X", "T", -200)
        with self.assertRaises(ValueError):
            shortest_path(graph, "A", "T")

    def test_a_nan_edge_cost_is_rejected(self) -> None:
        """NaN is never less than, equal to, or greater than anything.

        The edge is in a part of the graph the search never reaches, so only the
        check over every edge can catch it.
        """
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("C", "D", math.nan)
        with self.assertRaises(ValueError):
            shortest_path(graph, "A", "B")

    def test_works_on_a_long_chain_of_vertices(self) -> None:
        """A path through 10,001 vertices comes back complete and in order."""
        graph: DirectedGraph[int] = DirectedGraph()
        for i in range(10_000):
            graph.add_edge(i, i + 1, 1)
        self.assertEqual(shortest_path(graph, 0, 10_000), list(range(10_001)))


if __name__ == "__main__":
    unittest.main()
