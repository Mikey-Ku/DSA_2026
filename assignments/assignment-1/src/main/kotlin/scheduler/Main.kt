package scheduler

/**
 * Runs both conflict checks on the two example schedules from day 1 and prints
 * what each one finds.
 */
fun main() {
    val schedules = mapOf(
        "Schedule with a conflict" to listOf(
            meeting("A", "10:00", "11:00"),
            meeting("B", "13:00", "14:00"),
            meeting("C", "10:45", "11:30"),
        ),
        "Schedule with no conflict" to listOf(
            meeting("A", "10:00", "11:00"),
            meeting("B", "11:00", "11:30"),
            meeting("C", "13:00", "14:00"),
        ),
    )

    for ((name, meetings) in schedules) {
        println(name)
        for (meeting in meetings) {
            println("  $meeting")
        }
        println("  Checking pairs: ${conflictByPairs(meetings) ?: "no conflict"}")
        println("  Sorting first:  ${conflictBySort(meetings) ?: "no conflict"}")
        println()
    }
}
