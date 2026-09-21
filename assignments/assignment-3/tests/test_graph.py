"""Tests for DirectedGraph."""

import unittest

from graphs.graph import DirectedGraph


class DirectedGraphTest(unittest.TestCase):
    """Checks each graph operation on small, hand-built graphs."""

    def test_new_graph_is_empty(self) -> None:
        """A new graph has no vertices or edges."""
        graph: DirectedGraph[str] = DirectedGraph()
        self.assertEqual(graph.get_vertices(), set[str]())
        self.assertEqual(graph.get_edges("A"), {})

    def test_adding_an_edge_adds_both_vertices(self) -> None:
        """Both ends of an edge become vertices, even the one with no edges of its own.

        Asking about a vertex that is not there never creates it.
        """
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 1)
        self.assertEqual(graph.get_edges("Z"), {})
        self.assertEqual(graph.get_vertices(), {"A", "B"})

    def test_get_edges_returns_every_edge_leaving_a_vertex(self) -> None:
        """get_edges gives every neighbor of a vertex, along with each edge's cost.

        An edge only goes one way, so C has edges leading to it but none leaving.
        """
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("A", "C", 2.5)
        graph.add_edge("B", "C", 4)
        self.assertEqual(graph.get_edges("A"), {"B": 1, "C": 2.5})
        self.assertEqual(graph.get_edges("B"), {"C": 4})
        self.assertEqual(graph.get_edges("C"), {})

    def test_edges_in_opposite_directions_are_separate(self) -> None:
        """Edges from A to B and from B to A can have different costs."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("B", "A", 7)
        self.assertEqual(graph.get_edges("A"), {"B": 1})
        self.assertEqual(graph.get_edges("B"), {"A": 7})

    def test_adding_an_existing_edge_replaces_its_cost(self) -> None:
        """There is only ever one edge from one vertex to another."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 5)
        graph.add_edge("A", "B", 3)
        self.assertEqual(graph.get_edges("A"), {"B": 3})

    def test_a_vertex_can_have_an_edge_to_itself(self) -> None:
        """A self loop adds one vertex with an edge back to itself."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "A", 1)
        self.assertEqual(graph.get_vertices(), {"A"})
        self.assertEqual(graph.get_edges("A"), {"A": 1})

    def test_clear_removes_everything(self) -> None:
        """clear removes every vertex and edge, and the graph still works afterward."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("B", "C", 1)
        graph.clear()
        self.assertEqual(graph.get_vertices(), set[str]())
        self.assertEqual(graph.get_edges("A"), {})

        graph.add_edge("C", "D", 2)
        self.assertEqual(graph.get_vertices(), {"C", "D"})

    def test_returned_vertices_and_edges_are_copies(self) -> None:
        """Changing the graph doesn't change what it returned earlier, and the other way around."""
        graph: DirectedGraph[str] = DirectedGraph()
        graph.add_edge("A", "B", 1)
        vertices = graph.get_vertices()
        edges = graph.get_edges("A")

        graph.add_edge("A", "C", 1)
        self.assertEqual(vertices, {"A", "B"})
        self.assertEqual(edges, {"B": 1})

        vertices.add("Z")
        edges["Z"] = 5
        self.assertNotIn("Z", graph.get_vertices())
        self.assertNotIn("Z", graph.get_edges("A"))

    def test_vertices_can_be_any_hashable_type(self) -> None:
        """Tuples work as vertices, like the grid cells in the Project Euler problems."""
        graph: DirectedGraph[tuple[int, int]] = DirectedGraph()
        graph.add_edge((0, 0), (0, 1), 1)
        self.assertEqual(graph.get_vertices(), {(0, 0), (0, 1)})
        self.assertEqual(graph.get_edges((0, 0)), {(0, 1): 1})


if __name__ == "__main__":
    unittest.main()
