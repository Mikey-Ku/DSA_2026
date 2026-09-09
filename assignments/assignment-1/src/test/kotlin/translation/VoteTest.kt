package translation

import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertNull
import kotlin.test.assertTrue

/**
 * Build a set of ranked votes for a two-candidate race.
 *
 * @param alice Votes naming only Alice.
 * @param bob Votes naming only Bob.
 * @param aliceBob Votes ranking Alice first, then Bob.
 * @param bobAlice Votes ranking Bob first, then Alice.
 */
private fun aliceBobVotes(
    alice: Int = 0,
    bob: Int = 0,
    aliceBob: Int = 0,
    bobAlice: Int = 0,
): List<List<String>> = buildList {
    repeat(alice) { add(listOf("Alice")) }
    repeat(bob) { add(listOf("Bob")) }
    repeat(aliceBob) { add(listOf("Alice", "Bob")) }
    repeat(bobAlice) { add(listOf("Bob", "Alice")) }
}

/** The two ways of holding the election, which must always agree. */
private val IMPLEMENTATIONS: List<Pair<String, (List<String>, List<List<String>>) -> ElectionResult>> =
    listOf(
        "recursive" to ::holdAlternativeVote,
        "iterative" to ::holdIterativeVote,
    )

/**
 * Run an assertion against both implementations, and both with votes in their
 * given order and shuffled.
 *
 * Shuffling should never change the outcome, which is exactly the kind of thing
 * worth asserting rather than assuming.
 */
private fun forEachImplementation(
    candidates: List<String>,
    votes: List<List<String>>,
    check: (label: String, result: ElectionResult) -> Unit,
) {
    for ((name, implementation) in IMPLEMENTATIONS) {
        for (seed in listOf(null, 1, 2, 3)) {
            val orderedVotes = if (seed == null) votes else votes.shuffled(Random(seed))
            val label = "$name, shuffle=$seed:"
            check(label, implementation(candidates, orderedVotes))
        }
    }
}

class TallyVotesTest {
    @Test
    fun `each vote counts once, for its highest-ranked surviving candidate`() {
        val counts = tallyVotes(
            candidates = listOf("Alice", "Bob"),
            rankedVotes = aliceBobVotes(alice = 2, bob = 3, aliceBob = 1, bobAlice = 4),
        )
        assertEquals(mapOf("Alice" to 3, "Bob" to 7), counts)
    }

    @Test
    fun `eliminated candidates transfer their votes down the ranking`() {
        val votes = listOf(
            listOf("Charlie", "Alice"),
            listOf("Charlie", "Bob"),
            listOf("Alice"),
        )
        // With Charlie eliminated, the first two votes fall through.
        assertEquals(
            mapOf("Alice" to 2, "Bob" to 1),
            tallyVotes(listOf("Alice", "Bob"), votes),
        )
    }

    @Test
    fun `a vote whose candidates are all eliminated counts for nobody`() {
        val counts = tallyVotes(listOf("Alice"), listOf(listOf("Bob", "Charlie")))
        assertEquals(mapOf("Alice" to 0), counts)
        assertEquals(0, counts.values.sum())
    }

    @Test
    fun `every candidate appears even with no votes at all`() {
        assertEquals(
            mapOf("Alice" to 0, "Bob" to 0),
            tallyVotes(listOf("Alice", "Bob"), emptyList()),
        )
    }
}

class GetMinimumCandidateTest {
    @Test
    fun `returns the candidate with the fewest votes`() {
        assertEquals(
            "Bob",
            getMinimumCandidate(mapOf("Alice" to 10, "Bob" to 2, "Charlie" to 7)),
        )
    }

    @Test
    fun `breaks ties by order of appearance`() {
        assertEquals("Alice", getMinimumCandidate(mapOf("Alice" to 1, "Bob" to 1)))
        assertEquals("Bob", getMinimumCandidate(mapOf("Bob" to 1, "Alice" to 1)))
    }

    @Test
    fun `returns null when there are no candidates`() {
        assertNull(getMinimumCandidate(emptyMap()))
    }
}

class SimpleMajorityTest {
    private val cases = listOf(
        Triple("unanimous, all ranking the winner first", aliceBobVotes(aliceBob = 100), ElectionResult("Alice", 100)),
        Triple("unanimous, no votes for the other candidate", aliceBobVotes(bob = 100), ElectionResult("Bob", 100)),
        Triple("unanimous with a mix of votes", aliceBobVotes(alice = 50, aliceBob = 50), ElectionResult("Alice", 100)),
        Triple("won by one, ranked votes only", aliceBobVotes(aliceBob = 50, bobAlice = 51), ElectionResult("Bob", 51)),
        Triple("won by one, single votes only", aliceBobVotes(alice = 51, bob = 50), ElectionResult("Alice", 51)),
        Triple("won by one, mixed votes", aliceBobVotes(alice = 25, bob = 25, aliceBob = 25, bobAlice = 26), ElectionResult("Bob", 51)),
    )

    @Test
    fun `a simple majority wins outright`() {
        for ((description, votes, expected) in cases) {
            forEachImplementation(listOf("Alice", "Bob"), votes) { label, result ->
                assertEquals(expected, result, "$description ($label)")
            }
        }
    }
}

class TieTest {
    private val cases = listOf(
        "tie with single votes" to aliceBobVotes(alice = 150, bob = 150),
        "tie with ranked votes" to aliceBobVotes(aliceBob = 75, bobAlice = 75),
        "tie with mixed votes" to aliceBobVotes(alice = 50, bob = 50, aliceBob = 50, bobAlice = 50),
    )

    @Test
    fun `a tie still produces a winner with the right vote count`() {
        for ((description, votes) in cases) {
            forEachImplementation(listOf("Alice", "Bob"), votes) { label, result ->
                assertTrue(
                    result.winner in listOf("Alice", "Bob"),
                    "$description ($label): unexpected winner ${result.winner}",
                )
                assertEquals(150, result.votes, "$description ($label)")
            }
        }
    }
}

class RunoffTest {
    @Test
    fun `votes transfer once`() {
        val votes = buildList {
            repeat(50) { add(listOf("Bob", "Alice", "Charlie")) }
            repeat(26) { add(listOf("Charlie", "Alice", "Bob")) }
            repeat(25) { add(listOf("Alice", "Charlie", "Bob")) }
        }
        forEachImplementation(listOf("Alice", "Bob", "Charlie"), votes) { label, result ->
            assertEquals(ElectionResult("Charlie", 51), result, label)
        }
    }

    @Test
    fun `an outright majority wins a three-way race in the first round`() {
        val votes = buildList {
            repeat(51) { add(listOf("Bob", "Alice", "Charlie")) }
            repeat(25) { add(listOf("Charlie", "Alice", "Bob")) }
            repeat(25) { add(listOf("Alice", "Bob", "Charlie")) }
        }
        forEachImplementation(listOf("Alice", "Bob", "Charlie"), votes) { label, result ->
            assertEquals(ElectionResult("Bob", 51), result, label)
        }
    }

    @Test
    fun `votes transfer twice in the Tennessee capital election`() {
        val candidates = listOf("Memphis", "Nashville", "Chattanooga", "Knoxville")
        val votes = buildList {
            repeat(42) { add(listOf("Memphis", "Nashville", "Chattanooga", "Knoxville")) }
            repeat(26) { add(listOf("Nashville", "Chattanooga", "Knoxville", "Memphis")) }
            repeat(15) { add(listOf("Chattanooga", "Knoxville", "Nashville", "Memphis")) }
            repeat(17) { add(listOf("Knoxville", "Chattanooga", "Nashville", "Memphis")) }
        }
        forEachImplementation(candidates, votes) { label, result ->
            assertEquals(ElectionResult("Knoxville", 58), result, label)
        }
    }

    @Test
    fun `a lone candidate wins with the votes that name them`() {
        val votes = listOf(listOf("Alice"), listOf("Bob"), listOf("Bob", "Alice"))
        forEachImplementation(listOf("Alice"), votes) { label, result ->
            assertEquals(ElectionResult("Alice", 2), result, label)
        }
    }

    @Test
    fun `an empty candidate list is rejected`() {
        assertFailsWith<IllegalArgumentException> { holdAlternativeVote(emptyList(), emptyList()) }
        assertFailsWith<IllegalArgumentException> { holdIterativeVote(emptyList(), emptyList()) }
    }
}

class RefactoringEquivalenceTest {
    /**
     * The recursive and iterative versions must behave identically. That is a
     * property worth checking directly rather than case by case, so this throws
     * randomly generated elections at both and requires that they agree.
     */
    @Test
    fun `the recursive and iterative implementations agree on random elections`() {
        val random = Random(seed = 2026)
        val pool = listOf("Alice", "Bob", "Charlie", "Dana", "Eli", "Fran")

        repeat(300) { trial ->
            val candidates = pool.shuffled(random).take(random.nextInt(1, pool.size + 1))
            val votes = List(random.nextInt(0, 40)) {
                candidates.shuffled(random).take(random.nextInt(1, candidates.size + 1))
            }
            assertEquals(
                holdIterativeVote(candidates, votes),
                holdAlternativeVote(candidates, votes),
                "trial $trial disagreed for candidates=$candidates votes=$votes",
            )
        }
    }

    @Test
    fun `deep recursion does not overflow the stack`() {
        // holdAlternativeVote is tailrec, so eliminating thousands of candidates
        // one per round compiles to a loop instead of nesting stack frames.
        val candidates = List(3000) { "Candidate $it" }
        assertEquals(
            ElectionResult("Candidate 2999", 0),
            holdAlternativeVote(candidates, emptyList()),
        )
    }
}
