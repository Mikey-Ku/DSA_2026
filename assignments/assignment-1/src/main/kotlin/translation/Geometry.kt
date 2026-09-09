package translation

// Library of various helper functions for the recursive art problem.

import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.hypot
import kotlin.math.sin

/** A point in the two-dimensional plane. */
data class Point(val x: Double, val y: Double)

/**
 * Calculate the distance between two points.
 *
 * @param start The point to measure from.
 * @param end The point to measure to.
 * @return The distance between [start] and [end].
 */
fun dist(start: Point, end: Point): Double = hypot(end.x - start.x, end.y - start.y)

/**
 * Calculate the angle between two points in degrees.
 *
 * @param start The starting point to measure the angle from.
 * @param end The ending point to measure the angle to.
 * @return The angle between [start] and [end] in degrees.
 */
fun degrees(start: Point, end: Point): Double =
    Math.toDegrees(atan2(end.y - start.y, end.x - start.x))

/**
 * Calculate the point a set distance and angle from another point.
 *
 * @param start The point to calculate from.
 * @param distFromStart The distance from [start] that the returned point should
 *     be.
 * @param degreesFromStart The angle from [start] that the returned point should
 *     be.
 * @return The coordinates of the point that is [distFromStart] and
 *     [degreesFromStart] from [start].
 */
fun addDistDegrees(start: Point, distFromStart: Double, degreesFromStart: Double): Point {
    val angleRadians = Math.toRadians(degreesFromStart)
    return Point(
        x = start.x + distFromStart * cos(angleRadians),
        y = start.y + distFromStart * sin(angleRadians),
    )
}
