"""
Library to generate the points for a Koch snowflake of a given iteration.
"""

from recursive_art_helper import dist, degrees, add_dist_degrees


def transform_segment(start_point, end_point):
    """
    Transform a line segment of the Koch snowflake to get the points in the next
    iteration.

    Given a starting and ending point of a single line segment in the Koch
    snowflake, calculate the points that would be in the next iteration of the
    snowflake. The transformed segment has exactly five points, where the first
    and last points are start_point and end_point, respectively. The point after
    start_point and the point before end_point are a third and two thirds of the
    way between start_point and end_point, respectively. The middle point is
    placed in such a way that it forms an equilateral triangle with the second
    and fourth points in the transformed segment, always lying counterclockwise
    from the original segment (with end_point rotating about start_point).

    Args:
        start_point: The point representing the start of the segment.
        end_point: The point representing the end of the segment.

    Returns:
        A list of points in the transformed segment.
    """
    distance = dist(start_point, end_point)
    degree = degrees(start_point, end_point)
    point1 = add_dist_degrees(start_point, distance * 1 / 3, degree)
    point2 = add_dist_degrees(start_point, distance * 2 / 3, degree)
    point3 = add_dist_degrees(point1, distance * 1 / 3, 60 + degree)
    return [start_point, point1, point3, point2, end_point]


def make_snowflake(points, depth):
    """
    Generate the points for a given iteration of the Koch snowflake.

    Args:
        points: A list of points (2-tuples of ints/floats) in the snowflake.
        depth: An int representing how many more iterations of the snowflake to
            generate before returning.

    Returns:
        A list of points representing the points of the snowflake for the given
        depth.
    """
    if depth == 0:
        return points
    new_points = []

    for i in range(len(points) - 1):
        start_point = points[i]
        end_point = points[i + 1]
        transformed = transform_segment(start_point, end_point)
        new_points += transformed[:-1]
    new_points.append(points[-1])
    return make_snowflake(new_points, depth - 1)
