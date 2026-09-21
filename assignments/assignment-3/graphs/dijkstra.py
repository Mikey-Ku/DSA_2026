"""Dijkstra's algorithm for finding the cheapest path between two vertices."""

import math
from collections.abc import Hashable

from graphs.graph import DirectedGraph
from graphs.priority_queue import PriorityQueue


def shortest_path[V: Hashable](graph: DirectedGraph[V], start: V, target: V) -> list[V] | None:
    """Finds the cheapest path from start to target using Dijkstra's algorithm.

    Returns the vertices along the path (from start to target), or None if
    there is no path.
    """
    # Step 1: check the graph for negative or NaN edge costs
    vertices = graph.get_vertices()
    for vertex in vertices:
        for neighbor, cost in graph.get_edges(vertex).items():
            if cost < 0 or math.isnan(cost):
                raise ValueError(
                    "Dijkstra's algorithm needs edge costs of zero or more"
                )
    if start not in vertices or target not in vertices:
        return None

    # Step 2: Start with the start vertex
    distance: dict[V, float] = {start: 0.0}  
    previous: dict[V, V] = {} 
    finished: set[V] = set()
    queue: PriorityQueue[V] = PriorityQueue()
    queue.add_with_priority(start, 0.0)

    # Step 3: take the closest vertex out of the queue, over and over.
    while True:
        current = queue.next()
        if current is None:
            break
        if current == target:
            return _follow_back(previous, target)
        finished.add(current)
        
        # Step 4: check whether this vertex is a cheaper way to reach each neighbor.
        for neighbor, cost in graph.get_edges(current).items():
            if neighbor in finished:
                continue
            new_distance = distance[current] + cost
            old_distance = distance.get(neighbor)
            if old_distance is not None and new_distance >= old_distance:
                continue
            distance[neighbor] = new_distance
            previous[neighbor] = current
            if old_distance is None:
                queue.add_with_priority(neighbor, new_distance)  # first path found
            else:
                queue.adjust_priority(neighbor, new_distance)  # cheaper path found
    return None


def _follow_back[V: Hashable](previous: dict[V, V], target: V) -> list[V]:
    """Rebuilds the path by following previous back from target to the start."""
    path = [target]
    while path[-1] in previous:
        path.append(previous[path[-1]])
    path.reverse()
    return path
