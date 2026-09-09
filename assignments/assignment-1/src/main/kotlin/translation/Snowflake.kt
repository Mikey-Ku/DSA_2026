package translation

/** The interior angle of the equilateral bump added to each segment. */
private const val BUMP_ANGLE_DEGREES = 60.0

/** Each iteration divides a segment into thirds. */
private const val ONE_THIRD = 1.0 / 3.0
private const val TWO_THIRDS = 2.0 / 3.0

/**
 * Transform one line segment of a Koch snowflake into the next iteration.
 *
 * The transformed segment has exactly five points. The first and last are
 * [startPoint] and [endPoint]. The second and fourth lie one third and two
 * thirds of the way along the original segment. The middle point is placed so
 * that it forms an equilateral triangle with the second and fourth points,
 * always lying counterclockwise from the original segment.
 *
 * @param startPoint The point representing the start of the segment.
 * @param endPoint The point representing the end of the segment.
 * @return The five points of the transformed segment, in order.
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
 * Every segment in [points] is replaced by its five-point transformation, and
 * the process repeats [depth] times. A depth of zero returns [points] unchanged.
 *
 * This is marked `tailrec`, so the compiler rewrites the recursion into a loop
 * rather than consuming a stack frame per iteration.
 *
 * @param points The points of the snowflake so far, in order. Must not be empty.
 * @param depth How many further iterations to generate. Must not be negative.
 * @return The points of the snowflake at the requested depth.
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
        // Drop the last point of each transformed segment: it is the same as
        // the first point of the next one, and would otherwise be duplicated.
        transformedPoints += transformSegment(points[index], points[index + 1]).dropLast(1)
    }
    transformedPoints += points.last()

    return makeSnowflake(transformedPoints, depth - 1)
}
