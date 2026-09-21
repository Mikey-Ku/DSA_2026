from collections.abc import Hashable

class DirectedGraph[V: Hashable]:
    """A directed, weighted graph stored as an adjacency map.

    Each vertex maps to a dictionary of its outgoing edges, which maps each
    neighbor to the cost of the edge that leads there.
    """

    def __init__(self) -> None:
        """Creates an empty graph."""
        self._edges: dict[V, dict[V, float]] = {}

    def get_vertices(self) -> set[V]:
        """Gets every verticies in the graph.

        Returns:
            A new set of the vertices
        """
        return set(self._edges)

    def add_edge(self, from_vertex: V, to_vertex: V, cost: float) -> None:
        """Adds an edge from one vertex to another.

        Args:
            from_vertex: The vertex the edge starts at.
            to_vertex: The vertex the edge leads to.
            cost: The weight of the edge.
        """
        if from_vertex not in self._edges:
            self._edges[from_vertex] = {}
        self._edges[from_vertex][to_vertex] = cost
        if to_vertex not in self._edges:
            self._edges[to_vertex] = {}

    def get_edges(self, from_vertex: V) -> dict[V, float]:
        """Gets all the edges that begin at a vertex.

        Args:
            from_vertex: The vertex the edges start at.

        Returns:
            A new dictionary from each neighbor to the cost of the edge that
            leads there. It is empty if from_vertex is not in the graph.
        """
        return dict(self._edges.get(from_vertex, {}))

    def clear(self) -> None:
        """Removes every edge and vertex from the graph."""
        self._edges.clear()
