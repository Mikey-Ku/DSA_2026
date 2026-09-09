package translation

import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.hypot
import kotlin.math.sin

/** A point in the two-dimensional plane. */
data class Point(val x: Double, val y: Double)

/**
 * Calculate the straight-line distance between two points.
 *
 * Built on `hypot` rather than a literal `sqrt(dx * dx + dy * dy)`, which avoids
 * overflowing or underflowing for extreme coordinates.
 *
 * @param start The point to measure from.
 * @param end The point to measure to.
 * @return The Euclidean distance between [start] and [end].
 */
fun dist(start: Point, end: Point): Double = hypot(end.x - start.x, end.y - start.y)

/**
 * Calculate the angle from one point to another, in degrees.
 *
 * @param start The point to measure the angle from.
 * @param end The point to measure the angle to.
 * @return The angle from [start] to [end] in degrees, in the range (-180, 180].
 */
fun degrees(start: Point, end: Point): Double =
    Math.toDegrees(atan2(end.y - start.y, end.x - start.x))

/**
 * Calculate the point a given distance and angle away from another point.
 *
 * @param start The point to calculate from.
 * @param distFromStart How far from [start] the returned point should be.
 * @param degreesFromStart The angle from [start], in degrees, at which the
 *     returned point should lie.
 * @return The point that is [distFromStart] away from [start] at an angle of
 *     [degreesFromStart].
 */
fun addDistDegrees(start: Point, distFromStart: Double, degreesFromStart: Double): Point {
    val angleRadians = Math.toRadians(degreesFromStart)
    return Point(
        x = start.x + distFromStart * cos(angleRadians),
        y = start.y + distFromStart * sin(angleRadians),
    )
}
