"""
Library of various helper functions for the recursive art problem.
"""

import math

import matplotlib
import matplotlib.pyplot as plt

Point = tuple[float, float]


def _configure_plot():
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.axis("scaled")
    plt.grid(linestyle="--", zorder=0)
    plt.axhline(0, color="gray", linewidth=1, zorder=5)
    plt.axvline(0, color="gray", linewidth=1, zorder=5)


def plot_points(points: list[Point]):
    """
    Plot a series of two-dimensional points on a labeled grid.

    Args:
        points: The points to plot.
    """
    plt.plot(*list(zip(*points)), ".", markersize=12, zorder=10)
    _configure_plot()


def plot_path(points: list[Point]):
    """
    Plot a series of two-dimensional points as a path on a labeled grid.

    Args:
        points: The points to plot, in order.
    """
    plt.plot(*list(zip(*points)), zorder=10)
    _configure_plot()


def plot_snowflake(points: list[Point]) -> matplotlib.figure.Figure:
    """
    Create a plot of a Koch snowflake on a blank background.

    Args:
        points: The points of the snowflake to plot, in order.

    Returns:
        The matplotlib figure containing the plot of the snowflake.
    """
    plt.plot(*list(zip(*points)), zorder=10)
    plt.axis("scaled")
    plt.axis("off")
    return plt.gcf()


dist = math.dist


def degrees(start: Point, end: Point) -> float:
    """
    Calculate the angle between two points in degrees.

    Args:
        start: The starting point to measure the angle from.
        end: The ending point to measure the angle to.

    Returns:
        The angle between start and end in degrees.
    """
    x_start, y_start = start
    x_end, y_end = end
    angle_rads = math.atan2(y_end - y_start, x_end - x_start)
    return math.degrees(angle_rads)


def add_dist_degrees(
    start: Point, dist_from_start: float, degrees_from_start: float
) -> Point:
    """
    Calculate the point a set distance and angle from another point.

    Args:
        start: The point to calculate from.
        dist_from_start: The distance from start that the returned point should
            be.
        degrees_from_start: The angle from start that the returned point should
            be.

    Returns:
        The coordinates of the point that is dist and degrees from start.
    """
    x_start, y_start = start
    angle_rads = math.radians(degrees_from_start)
    x_diff = dist_from_start * math.cos(angle_rads)
    y_diff = dist_from_start * math.sin(angle_rads)
    return x_start + x_diff, y_start + y_diff
