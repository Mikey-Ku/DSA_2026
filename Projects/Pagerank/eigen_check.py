"""Check that PageRank is the eigenvector of the Google matrix for eigenvalue 1.

Builds the Google matrix G for a 1,000-page sample of web-Stanford, asks numpy
for its eigenvector, and compares it with the scores from pagerank().
"""

from collections import deque
from pathlib import Path

import numpy as np

from pagerank import load_graph, pagerank

DAMPING_FACTOR = 0.85
SAMPLE_START = 89073
SAMPLE_SIZE = 1000


def google_matrix(graph, damping_factor):
    """Build G = d * S + (1 - d) / N, where S is the link matrix."""
    pages = list(graph)
    index = {page: i for i, page in enumerate(pages)}
    n = len(pages)

    links_matrix = np.zeros((n, n))
    for page, links in graph.items():
        if links:
            # Column j puts 1/k on each of the k pages that page j links to.
            for link in links:
                links_matrix[index[link], index[page]] = 1 / len(links)
        else:
            # A dead end puts 1/N on every page.
            links_matrix[:, index[page]] = 1 / n

    # Add the random jumps to every entry.
    return pages, damping_factor * links_matrix + (1 - damping_factor) / n


def sample_graph(graph, start, size):
    """Take a smaller graph by following links out from one page, breadth-first."""
    pages = [start]
    seen = {start}
    queue = deque([start])

    while queue and len(pages) < size:
        page = queue.popleft()
        for link in sorted(graph[page]):
            if link not in seen and len(pages) < size:
                seen.add(link)
                pages.append(link)
                queue.append(link)

    # Keep only the links between pages in the sample.
    return {page: {link for link in graph[page] if link in seen} for page in pages}


def check(graph):
    """Compare numpy's eigenvector of G with the scores from pagerank()."""
    pages, google = google_matrix(graph, DAMPING_FACTOR)
    values, vectors = np.linalg.eig(google)

    # Take the eigenvector for the largest eigenvalue, which should be 1,
    # and scale it so the scores add up to 1.
    largest = np.argmax(np.abs(values))
    eigenvector = np.real(vectors[:, largest])
    eigenvector = eigenvector / eigenvector.sum()

    # Run the loop with a tight stopping point so it gets close to the exact answer.
    ranks, _ = pagerank(graph, DAMPING_FACTOR, tol=1.0e-12)
    gap = max(abs(ranks[page] - eigenvector[i]) for i, page in enumerate(pages))

    print(f"Pages: {len(pages)}")
    print(f"Largest eigenvalue: {abs(values[largest]):.4f}")
    print(f"Biggest difference from pagerank(): {gap:.1e}")


if __name__ == "__main__":
    stanford = load_graph(Path(__file__).parent / "web-Stanford.txt")
    check(sample_graph(stanford, SAMPLE_START, SAMPLE_SIZE))
