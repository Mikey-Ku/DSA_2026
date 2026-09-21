"""Project Euler problem 81, solved with Dijkstra's algorithm.
"""

from graphs.dijkstra import shortest_path
from graphs.graph import DirectedGraph

# A position in the matrix, as (row, column).
type Cell = tuple[int, int]


def smallest_path(matrix: list[list[int]]) -> list[Cell]:
    """Finds the path with the smallest sum, moving only right and down.

    Args:
        matrix: The rows of the matrix, from top to bottom.

    Returns:
        The cells along the path, from the top left to the bottom right.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    # A one cell matrix allows no moves, so it never gets an edge to search.
    if rows == 1 and cols == 1:
        return [(0, 0)]

    # Every cell is a vertex, and every move is an edge costing the number in next cell
    graph: DirectedGraph[Cell] = DirectedGraph()
    for row in range(rows):
        for col in range(cols):
            if row + 1 < rows:
                graph.add_edge((row, col), (row + 1, col), matrix[row + 1][col])
            if col + 1 < cols:
                graph.add_edge((row, col), (row, col + 1), matrix[row][col + 1])

    path = shortest_path(graph, (0, 0), (rows - 1, cols - 1))
    if path is None:
        raise RuntimeError("No path from the top left cell to the bottom right cell.")
    return path


def smallest_sum(matrix: list[list[int]]) -> int:
    """Adds up the cells of the cheapest path, which is the answer to the problem.

    Args:
        matrix: The rows of the matrix, from top to bottom.

    Returns:
        The smallest sum of any path from the top left to the bottom right.
    """
    return sum(matrix[row][col] for row, col in smallest_path(matrix))
