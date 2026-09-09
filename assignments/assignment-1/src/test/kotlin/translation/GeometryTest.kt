package translation

import kotlin.math.abs
import kotlin.math.sqrt
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

/** Absolute tolerance for floating-point comparisons throughout the tests. */
internal const val TOLERANCE = 1e-9

/**
 * Assert that two doubles are equal to within [TOLERANCE].
 *
 * The values under test are often very close to zero, where a purely relative
 * comparison behaves badly, so an absolute tolerance is used instead.
 */
internal fun assertClose(expected: Double, actual: Double, message: String = "") {
    assertTrue(
        abs(expected - actual) <= TOLERANCE,
        "$message expected <$expected> but was <$actual>",
    )
}

/** Assert that two points are equal to within [TOLERANCE] in both coordinates. */
internal fun assertPointClose(expected: Point, actual: Point, message: String = "") {
    assertClose(expected.x, actual.x, "$message x:")
    assertClose(expected.y, actual.y, "$message y:")
}

class DistTest {
    @Test
    fun `distance from a point to itself is zero`() {
        assertClose(0.0, dist(Point(3.0, -4.0), Point(3.0, -4.0)))
    }

    @Test
    fun `distance follows the 3-4-5 triangle`() {
        assertClose(5.0, dist(Point(0.0, 0.0), Point(3.0, 4.0)))
    }

    @Test
    fun `distance is symmetric`() {
        val start = Point(-2.5, 7.25)
        val end = Point(11.0, -3.75)
        assertClose(dist(start, end), dist(end, start))
    }

    @Test
    fun `distance handles negative coordinates`() {
        assertClose(sqrt(2.0), dist(Point(-1.0, -1.0), Point(-2.0, -2.0)))
    }
}

class DegreesTest {
    @Test
    fun `angle along the positive x axis is zero`() {
        assertClose(0.0, degrees(Point(0.0, 0.0), Point(5.0, 0.0)))
    }

    @Test
    fun `angle straight up is ninety degrees`() {
        assertClose(90.0, degrees(Point(0.0, 0.0), Point(0.0, 5.0)))
    }

    @Test
    fun `angle along the negative x axis is one hundred eighty degrees`() {
        assertClose(180.0, degrees(Point(0.0, 0.0), Point(-5.0, 0.0)))
    }

    @Test
    fun `angle straight down is negative ninety degrees`() {
        assertClose(-90.0, degrees(Point(0.0, 0.0), Point(0.0, -5.0)))
    }

    @Test
    fun `angle is measured relative to the start point`() {
        assertClose(45.0, degrees(Point(10.0, 10.0), Point(11.0, 11.0)))
    }
}

class AddDistDegreesTest {
    @Test
    fun `moving zero distance returns the start point`() {
        assertPointClose(Point(4.0, 9.0), addDistDegrees(Point(4.0, 9.0), 0.0, 137.0))
    }

    @Test
    fun `moving along the axes lands where expected`() {
        assertPointClose(Point(3.0, 0.0), addDistDegrees(Point(0.0, 0.0), 3.0, 0.0))
        assertPointClose(Point(0.0, 3.0), addDistDegrees(Point(0.0, 0.0), 3.0, 90.0))
        assertPointClose(Point(-3.0, 0.0), addDistDegrees(Point(0.0, 0.0), 3.0, 180.0))
    }

    @Test
    fun `dist and degrees invert addDistDegrees`() {
        val start = Point(-1.5, 2.5)
        val distance = 7.0
        val angle = 33.0

        val moved = addDistDegrees(start, distance, angle)

        assertClose(distance, dist(start, moved), "distance:")
        assertClose(angle, degrees(start, moved), "angle:")
    }
}

class PointTest {
    @Test
    fun `points with the same coordinates are equal`() {
        assertEquals(Point(1.0, 2.0), Point(1.0, 2.0))
    }

    @Test
    fun `points with different coordinates are not equal`() {
        assertTrue(Point(1.0, 2.0) != Point(2.0, 1.0))
    }
}
