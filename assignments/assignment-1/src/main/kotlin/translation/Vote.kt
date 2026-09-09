package translation

// Calculate the winner of an IRV election.

/**
 * The winning candidate's name and the number of votes they won with in the
 * final round.
 */
data class ElectionResult(val winner: String, val votes: Int)

/**
 * Calculate the number of votes received by each candidate in a round of an IRV
 * election.
 *
 * @param candidates A list representing the candidates still in the race.
 * @param rankedVotes A list of lists representing ranked votes for candidates,
 *     with each vote from most to least preferred.
 * @return A map from candidates to the number of votes they received.
 */
fun tallyVotes(
    candidates: List<String>,
    rankedVotes: List<List<String>>,
): Map<String, Int> {
    val remainingCandidates = candidates.toSet()
    val voteCounts = candidates.associateWithTo(LinkedHashMap()) { 0 }

    for (vote in rankedVotes) {
        val topChoice = vote.firstOrNull { it in remainingCandidates } ?: continue
        voteCounts[topChoice] = voteCounts.getValue(topChoice) + 1
    }
    return voteCounts
}

/**
 * Find and return the candidate who received the minimum number of votes.
 *
 * @param voteCounts A map from candidates to the number of votes received in
 *     this round of the IRV election.
 * @return The name of the candidate with the fewest votes, or `null` if
 *     [voteCounts] is empty.
 */
fun getMinimumCandidate(voteCounts: Map<String, Int>): String? =
    voteCounts.minByOrNull { it.value }?.key

/**
 * Determine the winner of an alternative (instant runoff) election.
 *
 * Given a list of candidates and ranked votes, hold an alternative vote election
 * and return the winning candidate and the number of votes they received in the
 * final round. Each ranked vote does not need to rank all of the candidates, but
 * if all of their chosen candidates are eliminated, the vote is not counted in
 * the total (for determining a majority winner).
 *
 * @param candidates A list of strings representing the candidates' names. Must
 *     not be empty.
 * @param rankedVotes A list of lists of strings representing the ranked votes for
 *     candidates, with each list in order from most to least preferred.
 * @return The winning candidate's name and the number of votes they won with in
 *     the final round.
 * @throws IllegalArgumentException If [candidates] is empty.
 */
tailrec fun holdAlternativeVote(
    candidates: List<String>,
    rankedVotes: List<List<String>>,
): ElectionResult {
    require(candidates.isNotEmpty()) { "An election needs at least one candidate." }

    if (candidates.size == 1) {
        val winner = candidates.first()
        return ElectionResult(winner, rankedVotes.count { winner in it })
    }

    val voteCounts = tallyVotes(candidates, rankedVotes)
    val totalVotes = voteCounts.values.sum()

    for ((candidate, numVotes) in voteCounts) {
        if (numVotes > totalVotes / 2) {
            return ElectionResult(candidate, numVotes)
        }
    }

    val minimumCandidate = getMinimumCandidate(voteCounts)
    return holdAlternativeVote(
        candidates.filter { it != minimumCandidate },
        rankedVotes,
    )
}

/**
 * Determine the winner of an alternative (instant runoff) election.
 *
 * This is the original, iterative implementation. It gives the same result as
 * [holdAlternativeVote].
 *
 * @param candidates A list of strings representing the candidates' names. Must
 *     not be empty.
 * @param rankedVotes A list of lists of strings representing the ranked votes for
 *     candidates, with each list in order from most to least preferred.
 * @return The winning candidate's name and the number of votes they won with in
 *     the final round.
 * @throws IllegalArgumentException If [candidates] is empty.
 */
fun holdIterativeVote(
    candidates: List<String>,
    rankedVotes: List<List<String>>,
): ElectionResult {
    require(candidates.isNotEmpty()) { "An election needs at least one candidate." }

    var remainingCandidates = candidates
    while (remainingCandidates.size > 1) {
        val voteCounts = tallyVotes(remainingCandidates, rankedVotes)
        val totalVotes = voteCounts.values.sum()

        for ((candidate, numVotes) in voteCounts) {
            if (numVotes > totalVotes / 2) {
                return ElectionResult(candidate, numVotes)
            }
        }

        val minimumCandidate = getMinimumCandidate(voteCounts)
        remainingCandidates = remainingCandidates.filter { it != minimumCandidate }
    }

    val winner = remainingCandidates.first()
    return ElectionResult(winner, rankedVotes.count { winner in it })
}
