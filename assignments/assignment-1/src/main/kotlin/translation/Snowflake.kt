package translation

// Library to generate the points for a Koch snowflake of a given iteration.

private const val BUMP_ANGLE_DEGREES = 60.0
private const val ONE_THIRD = 1.0 / 3.0
private const val TWO_THIRDS = 2.0 / 3.0

/**
 * Transform a line segment of the Koch snowflake to get the points in the next
 * iteration.
 *
 * Given a starting and ending point of a single line segment in the Koch
 * snowflake, calculate the points that would be in the next iteration of the
 * snowflake. The transformed segment has exactly five points, where the first
 * and last points are [startPoint] and [endPoint], respectively. The point after
 * [startPoint] and the point before [endPoint] are a third and two thirds of the
 * way between [startPoint] and [endPoint], respectively. The middle point is
 * placed in such a way that it forms an equilateral triangle with the second and
 * fourth points in the transformed segment, always lying counterclockwise from
 * the original segment (with [endPoint] rotating about [startPoint]).
 *
 * @param startPoint The point representing the start of the segment.
 * @param endPoint The point representing the end of the segment.
 * @return A list of points in the transformed segment.
 */
fun transformSegment(startPoint: Point, endPoint: Point): List<Point> {
    val segmentLength = dist(startPoint, endPoint)
    val segmentAngle = degrees(startPoint, endPoint)

    val oneThirdPoint = addDistDegrees(startPoint, segmentLength * ONE_THIRD, segmentAngle)
    val twoThirdsPoint = addDistDegrees(startPoint, segmentLength * TWO_THIRDS, segmentAngle)
    val peakPoint = addDistDegrees(
        oneThirdPoint,
        segmentLength * ONE_THIRD,
        segmentAngle + BUMP_ANGLE_DEGREES,
    )

    return listOf(startPoint, oneThirdPoint, peakPoint, twoThirdsPoint, endPoint)
}

/**
 * Generate the points for a given iteration of the Koch snowflake.
 *
 * @param points A list of points in the snowflake. Must not be empty.
 * @param depth How many more iterations of the snowflake to generate before
 *     returning. Must not be negative.
 * @return A list of points representing the points of the snowflake for the
 *     given depth.
 * @throws IllegalArgumentException If [points] is empty or [depth] is negative.
 */
tailrec fun makeSnowflake(points: List<Point>, depth: Int): List<Point> {
    require(points.isNotEmpty()) { "A snowflake needs at least one point." }
    require(depth >= 0) { "Depth must not be negative, but was $depth." }

    if (depth == 0) {
        return points
    }

    val transformedPoints = ArrayList<Point>(points.size * 4)
    for (index in 0 until points.size - 1) {
        transformedPoints += transformSegment(points[index], points[index + 1]).dropLast(1)
    }
    transformedPoints += points.last()

    return makeSnowflake(transformedPoints, depth - 1)
}
