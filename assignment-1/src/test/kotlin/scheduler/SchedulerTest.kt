package scheduler

import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import kotlin.test.assertTrue

/** The two conflict finders, so every behavioural test can run against both. */
private val FINDERS: List<Pair<String, (List<Meeting>) -> Conflict?>> = listOf(
    "pairwise" to ::findConflictByPairs,
    "sorting" to ::findConflictBySorting,
)

/**
 * Assert that both implementations agree on whether [meetings] conflict, and
 * that any conflict they report is a genuine one drawn from the input.
 *
 * Both algorithms answer the same question but may witness it with different
 * pairs, so the pair itself is checked for validity rather than for equality
 * between the two.
 *
 * @param meetings The schedule to check.
 * @param expectConflict Whether a conflict should be found.
 * @param message Context included in failure messages.
 */
private fun assertConflict(
    meetings: List<Meeting>,
    expectConflict: Boolean,
    message: String = "",
) {
    for ((name, findConflict) in FINDERS) {
        val conflict = findConflict(meetings)
        assertEquals(
            expectConflict,
            conflict != null,
            "$message [$name] on $meetings",
        )
        if (conflict != null) {
            assertTrue(
                conflict.earlier.overlaps(conflict.later),
                "$message [$name] reported a non-overlapping pair: $conflict",
            )
            assertTrue(
                conflict.earlier in meetings && conflict.later in meetings,
                "$message [$name] reported a pair not in the input: $conflict",
            )
            assertTrue(
                conflict.earlier !== conflict.later,
                "$message [$name] matched a meeting against itself: $conflict",
            )
        }
    }
}

class TimeParsingTest {
    @Test
    fun `clock times convert to minutes since midnight`() {
        assertEquals(0, timeOf("00:00"))
        assertEquals(600, timeOf("10:00"))
        assertEquals(645, timeOf("10:45"))
        assertEquals(1439, timeOf("23:59"))
    }

    @Test
    fun `formatting is the inverse of parsing`() {
        for (minute in 0 until 24 * 60) {
            assertEquals(minute, timeOf(formatTime(minute)))
        }
    }

    @Test
    fun `malformed times are rejected`() {
        for (bad in listOf("", "10", "10:00:00", "ten:00", "10:xx", "24:00", "10:60", "-1:00")) {
            assertFailsWith<IllegalArgumentException>("\"$bad\" should be rejected") {
                timeOf(bad)
            }
        }
    }
}

class MeetingTest {
    @Test
    fun `a meeting must end after it starts`() {
        assertFailsWith<IllegalArgumentException> { meeting("Zero length", "10:00", "10:00") }
        assertFailsWith<IllegalArgumentException> { meeting("Backwards", "11:00", "10:00") }
    }

    @Test
    fun `overlaps is symmetric`() {
        val morning = meeting("Morning", "10:00", "11:00")
        val overlapping = meeting("Overlapping", "10:45", "11:30")
        assertTrue(morning.overlaps(overlapping))
        assertTrue(overlapping.overlaps(morning))
    }

    @Test
    fun `a meeting overlaps itself`() {
        val standup = meeting("Standup", "10:00", "10:15")
        assertTrue(standup.overlaps(standup))
    }

    @Test
    fun `meetings print readably`() {
        assertEquals("Standup (10:00-10:15)", meeting("Standup", "10:00", "10:15").toString())
    }
}

class ConflictDetectionTest {
    @Test
    fun `the conflicting example from class is detected`() {
        // 10:00-11:00 and 10:45-11:30 overlap; 13:00-14:00 sits clear of both.
        assertConflict(
            listOf(
                meeting("A", "10:00", "11:00"),
                meeting("B", "13:00", "14:00"),
                meeting("C", "10:45", "11:30"),
            ),
            expectConflict = true,
        )
    }

    @Test
    fun `the conflict-free example from class is accepted`() {
        assertConflict(
            listOf(
                meeting("A", "10:00", "11:00"),
                meeting("B", "11:00", "11:30"),
                meeting("C", "13:00", "14:00"),
            ),
            expectConflict = false,
        )
    }

    @Test
    fun `a meeting ending exactly when another begins is not a conflict`() {
        // The edge case the problem calls out, and the reason the intervals are
        // half-open. Checked in both orders, since neither algorithm may assume
        // the input is sorted.
        val first = meeting("First", "09:00", "10:00")
        val second = meeting("Second", "10:00", "11:00")
        assertConflict(listOf(first, second), expectConflict = false, message = "in order:")
        assertConflict(listOf(second, first), expectConflict = false, message = "reversed:")
    }

    @Test
    fun `an overlap of a single minute is a conflict`() {
        assertConflict(
            listOf(
                meeting("First", "09:00", "10:01"),
                meeting("Second", "10:00", "11:00"),
            ),
            expectConflict = true,
        )
    }

    @Test
    fun `an empty schedule has no conflict`() {
        assertConflict(emptyList(), expectConflict = false)
    }

    @Test
    fun `a single meeting has no conflict`() {
        assertConflict(listOf(meeting("Only", "10:00", "11:00")), expectConflict = false)
    }

    @Test
    fun `two identical meetings conflict`() {
        val slot = meeting("Slot", "10:00", "11:00")
        assertConflict(listOf(slot, slot.copy(title = "Double booked")), expectConflict = true)
    }

    @Test
    fun `a meeting wholly inside another conflicts`() {
        assertConflict(
            listOf(
                meeting("All hands", "09:00", "17:00"),
                meeting("Standup", "10:00", "10:15"),
            ),
            expectConflict = true,
        )
    }

    @Test
    fun `two meetings starting at the same minute conflict`() {
        assertConflict(
            listOf(
                meeting("Short", "10:00", "10:15"),
                meeting("Long", "10:00", "11:00"),
            ),
            expectConflict = true,
        )
    }

    @Test
    fun `input order does not change the answer`() {
        val meetings = listOf(
            meeting("A", "08:00", "09:00"),
            meeting("B", "09:00", "10:00"),
            meeting("C", "10:00", "11:00"),
            meeting("D", "11:00", "12:00"),
        )
        val random = Random(seed = 7)
        repeat(20) {
            assertConflict(meetings.shuffled(random), expectConflict = false)
        }
    }

    @Test
    fun `a conflict at the very end of a long schedule is still found`() {
        val meetings = List(200) { meeting("Slot $it", formatTime(it * 4), formatTime(it * 4 + 4)) } +
            meeting("Latecomer", formatTime(199 * 4 + 2), formatTime(199 * 4 + 6))
        assertConflict(meetings, expectConflict = true)
    }

    @Test
    fun `sorting still finds a conflict when the overlapping pair is not adjacent`() {
        // Sorted by start: Long, Short1, Short2. The overlapping pair Long/Short2
        // is not adjacent, but Long/Short1 is, so checking neighbours suffices.
        val meetings = listOf(
            meeting("Long", "09:00", "17:00"),
            meeting("Short1", "09:10", "09:20"),
            meeting("Short2", "09:30", "09:40"),
        )
        val conflict = assertNotNull(findConflictBySorting(meetings))
        assertTrue(conflict.earlier.overlaps(conflict.later))
    }
}

class AlgorithmEquivalenceTest {
    /**
     * The two algorithms are different enough to be worth checking against each
     * other directly. This throws randomly generated schedules at both and
     * requires that they always reach the same verdict.
     */
    @Test
    fun `both algorithms agree on random schedules`() {
        val random = Random(seed = 2026)

        repeat(2000) { trial ->
            // A narrow day makes overlaps common, so both answers get exercised.
            val meetings = List(random.nextInt(0, 12)) { index ->
                val start = random.nextInt(0, 120)
                val length = random.nextInt(1, 30)
                Meeting("M$index", start, start + length)
            }
            assertEquals(
                hasConflictByPairs(meetings),
                hasConflictBySorting(meetings),
                "trial $trial disagreed on $meetings",
            )
        }
    }

    @Test
    fun `a schedule of back-to-back meetings is conflict-free at any size`() {
        val meetings = List(500) { Meeting("Slot $it", it * 2, it * 2 + 2) }
        assertNull(findConflictByPairs(meetings))
        assertNull(findConflictBySorting(meetings))
    }
}
