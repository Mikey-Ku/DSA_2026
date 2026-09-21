# Assignment 3: Graph Searching and Shortest Paths

Michael Ku

Data Structures and Algorithms, Fall 2026

## Part 1: Representing Graphs

`DirectedGraph` is in `graphs/graph.py`. Each vertex keeps a dictionary of the
vertices it has edges to and what each of those edges costs, so looking up one
vertex's edges is a single lookup.

- `get_vertices()` — every vertex in the graph
- `add_edge(from_vertex, to_vertex, cost)` — adds an edge, and both ends as vertices
- `get_edges(from_vertex)` — a vertex's neighbors and what each edge costs
- `clear()` — removes every vertex and edge

Tests are in `tests/test_graph.py`.

## Part 2: Creating a Priority Queue

`PriorityQueue` (`graphs/priority_queue.py`) is a wrapper around `MinHeap`
(`graphs/min_heap.py`). The heap is a binary tree kept in a list where every
parent's priority is at most its children's, so the smallest element is always at
the front, and adding or removing just moves one element up or down until that
rule holds again.

`PriorityQueue`:

- `is_empty()` — whether the queue has anything in it
- `add_with_priority(elem, priority)` — adds an element
- `next()` — removes and returns the lowest priority element
- `adjust_priority(elem, new_priority)` — changes an element's priority

`MinHeap` adds `insert`, `peek`, `remove_min`, and `change_priority`, and keeps a
dictionary from each element to its index in the list so `change_priority` can
find an element without searching for it.

Tests are in `tests/test_min_heap.py` and `tests/test_priority_queue.py`.

## Part 3: Searching

`shortest_path(graph, start, target)` in `graphs/dijkstra.py` uses Dijkstra's
algorithm to find the cheapest path between two vertices, or `None` if there is
no path. It keeps a best-known distance for every vertex and uses the priority
queue to always settle the closest one next, lowering its neighbors' distances
until the target comes out. 

Tests are in `tests/test_dijkstra.py`.

## Part 4: Solving Problems with Dijkstra

I chose [Project Euler problem 81](https://projecteuler.net/problem=81), which
asks for the path through a matrix with the smallest sum, moving only right and
down. `graphs/path_sums.py` makes every cell a vertex and every allowed move an
edge costing the number in the cell it leads into, so the cheapest path from the
top left to the bottom right is the answer.

- `smallest_path(matrix)` — the cells along the cheapest path
- `smallest_sum(matrix)` — the numbers in those cells added up

Tests are in `tests/test_path_sums.py`.
