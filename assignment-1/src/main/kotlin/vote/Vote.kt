package vote

/**
 * The outcome of an election.
 *
 * The Python original returned a bare `(str, int)` tuple, so every caller had to
 * remember which slot was which and unpack it positionally. Naming the fields
 * makes `result.votes` impossible to confuse with `result.winner`, and swapping
 * the two becomes a compile error instead of a silent bug.
 *
 * @property winner The name of the winning candidate.
 * @property votes The number of votes the winner received in the final round.
 */
data class ElectionResult(val winner: String, val votes: Int)

/**
 * Count the votes received by each candidate in one round of an IRV election.
 *
 * Each ranked vote is awarded to the highest-ranked candidate on it who is still
 * in the race. A vote whose candidates have all been eliminated counts for
 * nobody. Counting this way means eliminating a candidate never requires editing
 * the votes themselves.
 *
 * @param candidates The candidates still in the race.
 * @param rankedVotes The ranked votes, each ordered most to least preferred.
 * @return A map from each candidate to the number of votes they received, in the
 *     same order as [candidates].
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
 * Find the candidate who received the fewest votes.
 *
 * Ties are broken by whichever tied candidate appears first in [voteCounts].
 *
 * @param voteCounts A map from candidates to the votes they received this round.
 * @return The name of the candidate with the fewest votes, or `null` if
 *     [voteCounts] is empty.
 */
fun getMinimumCandidate(voteCounts: Map<String, Int>): String? =
    voteCounts.minByOrNull { it.value }?.key

/**
 * Determine the winner of an alternative (instant runoff) election, recursively.
 *
 * Each round, votes are tallied. If a candidate holds more than half of the
 * votes cast, they win. Otherwise the candidate with the fewest votes is
 * eliminated and the election is re-run with the remaining candidates. When only
 * one candidate is left, they win with however many votes still name them.
 *
 * A ranked vote need not rank every candidate. Once all of the candidates it
 * names are eliminated it stops counting toward the total, which is why a
 * majority is measured against the votes cast in that round rather than against
 * the size of [rankedVotes].
 *
 * This is the recursive rewrite of [holdIterativeVote], and the two are required
 * to agree on every input.
 *
 * @param candidates The candidates in the race. Must not be empty.
 * @param rankedVotes The ranked votes, each ordered most to least preferred.
 * @return The winning candidate and the votes they won with in the final round.
 * @throws IllegalArgumentException If [candidates] is empty.
 */
tailrec fun holdAlternativeVote(
    candidates: List<String>,
    rankedVotes: List<List<String>>,
): ElectionResult {
    require(candidates.isNotEmpty()) { "An election needs at least one candidate." }

    // Base case: one candidate left, so they win with every vote that names them.
    if (candidates.size == 1) {
        val winner = candidates.first()
        return ElectionResult(winner, rankedVotes.count { winner in it })
    }

    val voteCounts = tallyVotes(candidates, rankedVotes)
    val totalVotes = voteCounts.values.sum()

    // Base case: somebody holds an absolute majority of the votes cast.
    for ((candidate, numVotes) in voteCounts) {
        if (numVotes > totalVotes / 2) {
            return ElectionResult(candidate, numVotes)
        }
    }

    // Recursive case: drop the weakest candidate and run the election again.
    val minimumCandidate = getMinimumCandidate(voteCounts)
    return holdAlternativeVote(
        candidates.filter { it != minimumCandidate },
        rankedVotes,
    )
}

/**
 * Determine the winner of an alternative (instant runoff) election, iteratively.
 *
 * This is a direct translation of the loop-based implementation the assignment
 * supplied as the starting point. It is kept so the tests can assert that the
 * recursive rewrite in [holdAlternativeVote] produces identical results.
 *
 * @param candidates The candidates in the race. Must not be empty.
 * @param rankedVotes The ranked votes, each ordered most to least preferred.
 * @return The winning candidate and the votes they won with in the final round.
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
