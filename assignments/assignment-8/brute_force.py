"""Brute force nearest neighbor: check the distance to every point"""

from kd_tree import Point, squared_distance


def brute_force_nearest(points: list[Point], query: Point) -> Point:
    """The point closest to the query, found by checking all of them. Θ(nk)"""
    best = points[0]
    best_dist = squared_distance(query, best)
    for point in points:
        dist = squared_distance(query, point)
        if dist < best_dist:
            best = point
            best_dist = dist
    return best
