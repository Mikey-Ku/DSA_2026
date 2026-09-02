package scheduler

import kotlin.system.measureNanoTime

/** Schedule sizes to time, each double the last so the growth ratios are readable. */
private val SIZES = listOf(1_000, 2_000, 4_000, 8_000, 16_000)

/** Timed repetitions per size; the fastest run is reported. */
private const val REPETITIONS = 7

/**
 * Build a conflict-free schedule of [size] back-to-back meetings, shuffled.
 *
 * Conflict-free is deliberately the *worst* case. Both functions stop as soon
 * as they find a conflict, so a schedule that conflicts early would measure how
 * lucky the input was rather than how the algorithms scale. With no conflict at
 * all, the pairwise version must make every one of its n(n-1)/2 comparisons.
 *
 * The list is shuffled so the sorting version faces genuinely unordered input.
 *
 * @param size How many meetings to generate.
 * @return A shuffled, conflict-free schedule.
 */
private fun worstCaseSchedule(size: Int): List<Meeting> =
    List(size) { Meeting("Slot $it", it * 2, it * 2 + 2) }.shuffled()

/** Time [block] [REPETITIONS] times and return the fastest run, in milliseconds. */
private fun fastestMillis(block: () -> Unit): Double =
    (1..REPETITIONS).minOf { measureNanoTime(block) } / 1_000_000.0

/**
 * Time both conflict-detection algorithms on schedules of increasing size.
 *
 * This is indicative, not a rigorous benchmark — there is no JMH here, just a
 * warm-up and a best-of-five. It is enough to show the shapes apart: doubling n
 * should roughly quadruple the pairwise time and roughly double the sorting
 * time.
 */
fun main() {
    // Let the JIT compile both functions before anything is measured, otherwise
    // the first few timings mostly record the interpreter warming up.
    repeat(3) {
        val warmup = worstCaseSchedule(2_000)
        hasConflictByPairs(warmup)
        hasConflictBySorting(warmup)
    }

    println("Worst case (no conflicts), best of $REPETITIONS runs.")
    println()
    println("      n |   pairwise |  ratio |    sorting |  ratio")
    println("--------+------------+--------+------------+-------")

    var previousPairs: Double? = null
    var previousSort: Double? = null

    for (size in SIZES) {
        val schedule = worstCaseSchedule(size)
        // Warm up at this size too: the JIT keeps re-optimising as the input
        // grows, and without this the mid-range timings come out erratically low.
        hasConflictByPairs(schedule)
        hasConflictBySorting(schedule)

        val pairsMillis = fastestMillis { hasConflictByPairs(schedule) }
        val sortMillis = fastestMillis { hasConflictBySorting(schedule) }

        println(
            "%7d | %8.2f ms | %6s | %8.2f ms | %6s".format(
                size,
                pairsMillis,
                previousPairs?.let { "%.1fx".format(pairsMillis / it) } ?: "-",
                sortMillis,
                previousSort?.let { "%.1fx".format(sortMillis / it) } ?: "-",
            )
        )
        previousPairs = pairsMillis
        previousSort = sortMillis
    }

    println()
    println("Expect the pairwise ratio near 4.0 (n^2) and the sorting ratio near 2.0 (n log n).")
}
