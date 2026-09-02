package scheduler

/** Minutes in an hour, used when converting to and from clock times. */
private const val MINUTES_PER_HOUR = 60

/** Minutes in a day, the exclusive upper bound on any time of day. */
private const val MINUTES_PER_DAY = 24 * MINUTES_PER_HOUR

/**
 * Convert a `HH:MM` clock time into minutes since midnight.
 *
 * @param clockTime A 24-hour clock time such as `"09:00"` or `"13:45"`.
 * @return The number of minutes since midnight.
 * @throws IllegalArgumentException If [clockTime] is not a valid time of day.
 */
fun timeOf(clockTime: String): Int {
    val parts = clockTime.split(":")
    require(parts.size == 2) { "Expected a time of the form HH:MM, but got \"$clockTime\"." }

    val hours = parts[0].toIntOrNull()
    val minutes = parts[1].toIntOrNull()
    require(hours != null && minutes != null) {
        "Expected a time of the form HH:MM, but got \"$clockTime\"."
    }
    require(hours in 0..23) { "Hour must be between 00 and 23, but got $hours." }
    require(minutes in 0..59) { "Minute must be between 00 and 59, but got $minutes." }

    return hours * MINUTES_PER_HOUR + minutes
}

/**
 * Render minutes since midnight as a `HH:MM` clock time.
 *
 * @param minutesSinceMidnight A time of day in minutes since midnight.
 * @return The corresponding 24-hour clock time.
 */
fun formatTime(minutesSinceMidnight: Int): String {
    require(minutesSinceMidnight in 0 until MINUTES_PER_DAY) {
        "Time must fall within a single day, but got $minutesSinceMidnight."
    }
    val hours = minutesSinceMidnight / MINUTES_PER_HOUR
    val minutes = minutesSinceMidnight % MINUTES_PER_HOUR
    return "%02d:%02d".format(hours, minutes)
}

/**
 * A meeting occupying the half-open time interval `[start, end)`.
 *
 * Half-open is the whole trick to this problem. Because the end minute is
 * excluded, a meeting running 10:00-11:00 and one running 11:00-11:30 share no
 * minute at all, which is exactly the rule the problem asks for: a meeting
 * ending precisely when another begins is not a conflict.
 *
 * @property title A human-readable name, used only for reporting.
 * @property start The first minute of the meeting, as minutes since midnight.
 * @property end The first minute *after* the meeting, as minutes since midnight.
 */
data class Meeting(val title: String, val start: Int, val end: Int) {
    init {
        require(start < end) {
            "A meeting must end after it starts, but \"$title\" runs " +
                "${formatTime(start)}-${formatTime(end)}."
        }
    }

    /**
     * Report whether this meeting and [other] share at least one minute.
     *
     * Two half-open intervals overlap exactly when each starts before the other
     * ends. Note that both comparisons are strict: making either one `<=` would
     * wrongly flag back-to-back meetings as conflicting.
     *
     * @param other The meeting to compare against.
     * @return `true` if the two meetings overlap.
     */
    fun overlaps(other: Meeting): Boolean = start < other.end && other.start < end

    /** A compact form such as `Standup (10:00-10:15)`, for readable failures. */
    override fun toString(): String = "$title (${formatTime(start)}-${formatTime(end)})"
}

/**
 * Build a meeting from clock times.
 *
 * @param title A human-readable name for the meeting.
 * @param start The start time as `HH:MM`.
 * @param end The end time as `HH:MM`.
 * @return The corresponding [Meeting].
 */
fun meeting(title: String, start: String, end: String): Meeting =
    Meeting(title, timeOf(start), timeOf(end))

/**
 * Two meetings found to overlap.
 *
 * @property earlier The meeting that starts first, or the one found first when
 *     both start at the same minute.
 * @property later The other meeting in the conflicting pair.
 */
data class Conflict(val earlier: Meeting, val later: Meeting) {
    override fun toString(): String = "$earlier conflicts with $later"
}

/**
 * Find a conflicting pair by comparing every pair of meetings.
 *
 * The straightforward approach: for each meeting, compare it against every
 * later meeting in the list. Comparing against *later* meetings only, rather
 * than all of them, halves the work and avoids ever comparing a meeting with
 * itself.
 *
 * Runs in O(n^2) time and O(1) extra space. See `docs/meeting-scheduler.md`.
 *
 * @param meetings The meetings to check, in any order.
 * @return A conflicting pair, or `null` if no two meetings overlap.
 */
fun findConflictByPairs(meetings: List<Meeting>): Conflict? {
    for (i in meetings.indices) {
        for (j in i + 1 until meetings.size) {
            if (meetings[i].overlaps(meetings[j])) {
                return orderedConflict(meetings[i], meetings[j])
            }
        }
    }
    return null
}

/**
 * Find a conflicting pair by sorting the meetings by start time first.
 *
 * Once the meetings are in start-time order, only *neighbouring* pairs need
 * checking. That is not an approximation, it is exact: if any two meetings
 * overlap, then some neighbouring pair must also overlap. The argument is in
 * `docs/meeting-scheduler.md`.
 *
 * Runs in O(n log n) time, dominated by the sort, using Kotlin's built-in
 * [sortedBy] rather than a hand-written sort.
 *
 * @param meetings The meetings to check, in any order.
 * @return A conflicting pair, or `null` if no two meetings overlap.
 */
fun findConflictBySorting(meetings: List<Meeting>): Conflict? {
    val byStartTime = meetings.sortedBy { it.start }

    for (i in 1 until byStartTime.size) {
        val previous = byStartTime[i - 1]
        val current = byStartTime[i]
        // Sorting guarantees previous.start <= current.start, so the general
        // overlap test collapses to this single comparison.
        if (current.start < previous.end) {
            return Conflict(previous, current)
        }
    }
    return null
}

/**
 * Report whether any two meetings overlap, comparing every pair.
 *
 * @param meetings The meetings to check, in any order.
 * @return `true` if at least two meetings overlap.
 */
fun hasConflictByPairs(meetings: List<Meeting>): Boolean =
    findConflictByPairs(meetings) != null

/**
 * Report whether any two meetings overlap, by sorting first.
 *
 * @param meetings The meetings to check, in any order.
 * @return `true` if at least two meetings overlap.
 */
fun hasConflictBySorting(meetings: List<Meeting>): Boolean =
    findConflictBySorting(meetings) != null

/** Put a conflicting pair into start-time order, so reports read naturally. */
private fun orderedConflict(one: Meeting, other: Meeting): Conflict =
    if (one.start <= other.start) Conflict(one, other) else Conflict(other, one)
