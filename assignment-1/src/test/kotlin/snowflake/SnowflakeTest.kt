package snowflake

import geometry.Point
import geometry.TOLERANCE
import geometry.addDistDegrees
import geometry.assertClose
import geometry.assertPointClose
import geometry.degrees
import geometry.dist
import kotlin.math.abs
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertTrue

/** Build a random line segment from a seeded generator, for property-style checks. */
private fun randomSegment(seed: Int): Pair<Point, Point> {
    val random = Random(seed)
    fun coordinate() = random.nextDouble(-1.0, 1.0)
    return Point(coordinate(), coordinate()) to Point(coordinate(), coordinate())
}

/** Build an equilateral triangle, closed by repeating its first point. */
private fun randomTriangle(seed: Int): List<Point> {
    val (aPoint, bPoint) = randomSegment(seed)
    val cPoint = addDistDegrees(aPoint, dist(aPoint, bPoint), degrees(aPoint, bPoint) - 60.0)
    return listOf(aPoint, bPoint, cPoint, aPoint)
}

/** Total length of the path through a list of points. */
private fun pathLength(points: List<Point>): Double =
    (0 until points.size - 1).sumOf { dist(points[it], points[it + 1]) }

class TransformSegmentTest {
    @Test
    fun `transformed segment has exactly five points`() {
        for (seed in 1..20) {
            val (start, end) = randomSegment(seed)
            assertEquals(5, transformSegment(start, end).size, "seed $seed:")
        }
    }

    @Test
    fun `endpoints are preserved`() {
        for (seed in 1..20) {
            val (start, end) = randomSegment(seed)
            val transformed = transformSegment(start, end)
            assertPointClose(start, transformed.first(), "seed $seed start:")
            assertPointClose(end, transformed.last(), "seed $seed end:")
        }
    }

    @Test
    fun `second and fourth points sit one and two thirds along the segment`() {
        for (seed in 1..20) {
            val (start, end) = randomSegment(seed)
            val transformed = transformSegment(start, end)
            val segmentLength = dist(start, end)

            assertClose(segmentLength / 3.0, dist(start, transformed[1]), "seed $seed:")
            assertClose(segmentLength * 2.0 / 3.0, dist(start, transformed[3]), "seed $seed:")
            // Both must lie on the original segment, so the angle is unchanged.
            assertClose(degrees(start, end), degrees(start, transformed[1]), "seed $seed:")
            assertClose(degrees(start, end), degrees(start, transformed[3]), "seed $seed:")
        }
    }

    @Test
    fun `the four sub-segments are all one third of the original`() {
        for (seed in 1..20) {
            val (start, end) = randomSegment(seed)
            val transformed = transformSegment(start, end)
            val expectedLength = dist(start, end) / 3.0

            for (index in 0 until transformed.size - 1) {
                assertClose(
                    expectedLength,
                    dist(transformed[index], transformed[index + 1]),
                    "seed $seed sub-segment $index:",
                )
            }
        }
    }

    @Test
    fun `the peak forms an equilateral triangle with its neighbours`() {
        for (seed in 1..20) {
            val (start, end) = randomSegment(seed)
            val (_, oneThird, peak, twoThirds, _) = transformSegment(start, end)

            val sideA = dist(oneThird, peak)
            val sideB = dist(peak, twoThirds)
            val sideC = dist(oneThird, twoThirds)

            assertClose(sideC, sideA, "seed $seed:")
            assertClose(sideC, sideB, "seed $seed:")
        }
    }

    @Test
    fun `the peak lies counterclockwise from the original segment`() {
        for (seed in 1..20) {
            val (start, end) = randomSegment(seed)
            val peak = transformSegment(start, end)[2]

            // A positive cross product means peak is to the left of start->end.
            val crossProduct =
                (end.x - start.x) * (peak.y - start.y) - (end.y - start.y) * (peak.x - start.x)
            assertTrue(crossProduct > TOLERANCE, "seed $seed: peak was not counterclockwise")
        }
    }

    @Test
    fun `a known segment transforms to known points`() {
        val transformed = transformSegment(Point(0.0, 0.0), Point(3.0, 0.0))

        assertPointClose(Point(0.0, 0.0), transformed[0])
        assertPointClose(Point(1.0, 0.0), transformed[1])
        // The peak of an equilateral triangle on the middle third.
        assertPointClose(Point(1.5, 0.8660254037844386), transformed[2])
        assertPointClose(Point(2.0, 0.0), transformed[3])
        assertPointClose(Point(3.0, 0.0), transformed[4])
    }
}

class MakeSnowflakeTest {
    @Test
    fun `depth zero returns the original points unchanged`() {
        val triangle = randomTriangle(seed = 5)
        assertEquals(triangle, makeSnowflake(triangle, 0))
    }

    @Test
    fun `each iteration turns every segment into four`() {
        val triangle = randomTriangle(seed = 7)
        var expectedSegments = triangle.size - 1

        for (depth in 1..5) {
            expectedSegments *= 4
            assertEquals(
                expectedSegments + 1,
                makeSnowflake(triangle, depth).size,
                "depth $depth:",
            )
        }
    }

    @Test
    fun `each iteration multiplies the path length by four thirds`() {
        val triangle = randomTriangle(seed = 11)
        val baseLength = pathLength(triangle)

        for (depth in 0..5) {
            var expectedLength = baseLength
            repeat(depth) { expectedLength *= 4.0 / 3.0 }
            val actualLength = pathLength(makeSnowflake(triangle, depth))
            assertTrue(
                abs(expectedLength - actualLength) <= 1e-9 * expectedLength,
                "depth $depth: expected <$expectedLength> but was <$actualLength>",
            )
        }
    }

    @Test
    fun `the original points survive at evenly spaced indices`() {
        val triangle = randomTriangle(seed = 13)

        for (depth in 0..4) {
            val result = makeSnowflake(triangle, depth)
            var stride = 1
            repeat(depth) { stride *= 4 }

            for ((index, original) in triangle.withIndex()) {
                assertPointClose(original, result[index * stride], "depth $depth point $index:")
            }
        }
    }

    @Test
    fun `applying one iteration twice matches applying two at once`() {
        val triangle = randomTriangle(seed = 17)
        assertEquals(
            makeSnowflake(triangle, 2),
            makeSnowflake(makeSnowflake(triangle, 1), 1),
        )
    }

    @Test
    fun `a single point is returned unchanged at any depth`() {
        val single = listOf(Point(1.0, 2.0))
        assertEquals(single, makeSnowflake(single, 3))
    }

    @Test
    fun `negative depth is rejected`() {
        assertFailsWith<IllegalArgumentException> {
            makeSnowflake(randomTriangle(seed = 19), -1)
        }
    }

    @Test
    fun `empty input is rejected`() {
        assertFailsWith<IllegalArgumentException> { makeSnowflake(emptyList(), 1) }
    }

    @Test
    fun `deep recursion does not overflow the stack`() {
        // makeSnowflake is tailrec, so the compiler turns this into a loop.
        // The equivalent Python hits its recursion limit at around 1000 frames.
        val single = listOf(Point(0.0, 0.0))
        assertEquals(single, makeSnowflake(single, 1_000_000))
    }
}
