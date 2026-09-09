package scheduler

val MINUTES_PER_HOUR = 60
val MINUTES_PER_DAY = 24 * MINUTES_PER_HOUR

/**
 * Converts a clock time such as `10:45` into minutes since midnight.
 *
 * This gives the scheduler a simple number it can use when comparing times.
 */
fun timeOf(time: String): Int {
    val parts = time.split(":")
    require(parts.size == 2) {
        "Expected a time of the form HH:MM, but got \"$time\"."
    }
    val hours = parts[0].toIntOrNull()
    val minutes = parts[1].toIntOrNull()
    require(hours != null && minutes != null) {
        "Expected a time of the form HH:MM, but got \"$time\"."
    }
    require(hours in 0..23) {
        "Hour must be between 00 and 23, but got $hours."
    }
    require(minutes in 0..59) {
        "Minute must be between 00 and 59, but got $minutes."
    }
    return hours * MINUTES_PER_HOUR + minutes
}

/**
 * Converts minutes since midnight back into an easy-to-read clock time.
 */
fun formatTime(minuteOfDay: Int): String {
    require(minuteOfDay in 0 until MINUTES_PER_DAY) {
        "Time must fall within a single day, but got $minuteOfDay."
    }
    val hours = minuteOfDay / MINUTES_PER_HOUR
    val minutes = minuteOfDay % MINUTES_PER_HOUR
    return "%02d:%02d".format(hours, minutes)
}

/**
 * Stores the name, start time, and end time of one meeting.
 *
 * Start and end are stored as minutes since midnight. A meeting that ends at the
 * exact time another meeting begins does not count as a conflict.
 */
data class Meeting(
    val title: String,
    val start: Int,
    val end: Int,
) {
    init {
        require(start < end) {
            "A meeting must end after it starts, but \"$title\" runs " +
                "${formatTime(start)}-${formatTime(end)}."
        }
    }

    /**
     * Returns true when this meeting and the other meeting take place at the
     * same time for at least one minute.
     */
    fun overlaps(other: Meeting): Boolean {
        return start < other.end && other.start < end
    }

    /** Displays a meeting in a readable form such as `Standup (10:00-10:15)`. */
    override fun toString(): String {
        return "$title (${formatTime(start)}-${formatTime(end)})"
    }
}

/**
 * Creates a meeting using familiar clock-time strings instead of minute values.
 */
fun meeting(title: String, start: String, end: String): Meeting {
    return Meeting(title, timeOf(start), timeOf(end))
}

/**
 * Stores the two meetings involved in a scheduling conflict.
 */
data class Conflict(
    val earlier: Meeting,
    val later: Meeting,
) {
    override fun toString(): String {
        return "$earlier conflicts with $later"
    }
}

/**
 * Looks for a conflict by checking every possible pair of meetings.
 *
 * Returns the first conflict it finds, or null when the schedule has no conflict.
 */
fun conflictByPairs(meetings: List<Meeting>): Conflict? {
    for (i in meetings.indices) {
        for (j in i + 1 until meetings.size) {
            val first = meetings[i]
            val second = meetings[j]
            if (first.overlaps(second)) {
                return ordered(first, second)
            }
        }
    }
    return null
}

/**
 * Looks for a conflict by sorting meetings by start time and checking neighbors.
 *
 * Returns the first conflict it finds, or null when the schedule has no conflict.
 */
fun conflictBySort(meetings: List<Meeting>): Conflict? {
    val sorted = meetings.sortedBy { it.start }

    for (i in 1 until sorted.size) {
        val previous = sorted[i - 1]
        val current = sorted[i]
        if (current.start < previous.end) {
            return Conflict(previous, current)
        }
    }
    return null
}

/** Places the earlier meeting first so the conflict is easier to read. */
private fun ordered(one: Meeting, other: Meeting): Conflict {
    if (one.start <= other.start) {
        return Conflict(one, other)
    }

    return Conflict(other, one)
}
