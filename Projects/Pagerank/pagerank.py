"""PageRank on the web-Stanford graph from SNAP.

Loads the graph, runs PageRank with d = 0.85, and prints the top 10 pages.
"""

import time
from pathlib import Path


def pagerank(graph, damping_factor=0.85, max_iterations=1000, tol=1.0e-6):
    """Run PageRank on a graph and return the ranks and the number of passes."""
    num_pages = len(graph)

    # Start every page at 1 / N.
    pagerank_values = {page: 1 / num_pages for page in graph}

    # Dead ends link nowhere, so their score is spread over every page.
    dead_ends = [page for page in graph if not graph[page]]

    for passes in range(1, max_iterations + 1):
        # Every page starts the pass with the same base amount:
        # the random jump, (1 - d) / N, plus d of the dead ends' total score spread over all N pages.
        dead_end_rank = sum(pagerank_values[page] for page in dead_ends)
        base_rank = (1 - damping_factor) / num_pages + damping_factor * dead_end_rank / num_pages
        new_pagerank_values = {page: base_rank for page in graph}

        # Each page splits d of its score evenly among the pages it links to.
        for page, links in graph.items():
            if links:
                share = damping_factor * pagerank_values[page] / len(links)
                for link in links:
                    new_pagerank_values[link] += share

        # Stop once the total change in scores is below tol.
        total_change = sum(abs(new_pagerank_values[page] - pagerank_values[page]) for page in graph)
        pagerank_values = new_pagerank_values
        if total_change < tol:
            break

    return pagerank_values, passes


def top_pages(pagerank_values, count=10):
    """Return the highest-ranked pages, best first."""
    return sorted(pagerank_values.items(), key=lambda item: item[1], reverse=True)[:count]


def load_graph(filename):
    """Load a graph from a SNAP edge list file."""
    graph = {}

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            # Skip empty lines and dataset comments.
            if not line or line.startswith("#"):
                continue

            # Each line is one link: "from to".
            source, destination = map(int, line.split())

            # Give both pages an entry, even if they link nowhere.
            if source not in graph:
                graph[source] = set()

            if destination not in graph:
                graph[destination] = set()

            # Record the outgoing link.
            graph[source].add(destination)

    return graph


if __name__ == "__main__":
    graph = load_graph(Path(__file__).parent / "web-Stanford.txt")
    print("Pages:", len(graph))
    print("Links:", sum(len(links) for links in graph.values()))

    # Run PageRank and time it.
    start = time.time()
    pagerank_values, passes = pagerank(graph)
    print(f"d = 0.85 took {passes} passes and {time.time() - start:.1f} seconds")

    print("Top 10 pages:")
    for place, (page, rank) in enumerate(top_pages(pagerank_values), start=1):
        print(f"{place}. Page {page}: {rank:.6f}")
