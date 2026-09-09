package scheduler

private const val MINUTES_PER_HOUR = 60
private const val MINUTES_PER_DAY = 24 * MINUTES_PER_HOUR

/**
 * Converts a clock time such as `10:45` into minutes since midnight.
 *
 * This gives the scheduler a simple number it can use when comparing times.
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
 * Converts minutes since midnight back into an easy-to-read clock time.
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
        val thisMeetingStartsBeforeOtherEnds = start < other.end
        val otherMeetingStartsBeforeThisEnds = other.start < end

        return thisMeetingStartsBeforeOtherEnds && otherMeetingStartsBeforeThisEnds
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
    val startInMinutes = timeOf(start)
    val endInMinutes = timeOf(end)

    return Meeting(title, startInMinutes, endInMinutes)
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
fun findConflictByPairs(meetings: List<Meeting>): Conflict? {
    for (i in meetings.indices) {
        for (j in i + 1 until meetings.size) {
            val firstMeeting = meetings[i]
            val secondMeeting = meetings[j]

            if (firstMeeting.overlaps(secondMeeting)) {
                return orderedConflict(firstMeeting, secondMeeting)
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
fun findConflictBySorting(meetings: List<Meeting>): Conflict? {
    val byStartTime = meetings.sortedBy { meeting ->
        meeting.start
    }

    for (i in 1 until byStartTime.size) {
        val previous = byStartTime[i - 1]
        val current = byStartTime[i]
        // After sorting, compare the current meeting with the one before it.
        if (current.start < previous.end) {
            return Conflict(previous, current)
        }
    }
    return null
}

/**
 * Returns true when the pair-checking approach finds a conflict.
 */
fun hasConflictByPairs(meetings: List<Meeting>): Boolean {
    val conflict = findConflictByPairs(meetings)
    return conflict != null
}

/**
 * Returns true when the sorting approach finds a conflict.
 */
fun hasConflictBySorting(meetings: List<Meeting>): Boolean {
    val conflict = findConflictBySorting(meetings)
    return conflict != null
}

/** Places the earlier meeting first so the conflict is easier to read. */
private fun orderedConflict(one: Meeting, other: Meeting): Conflict {
    if (one.start <= other.start) {
        return Conflict(one, other)
    }

    return Conflict(other, one)
}
