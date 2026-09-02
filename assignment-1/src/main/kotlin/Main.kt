import geometry.Point
import kotlin.random.Random
import markov.buildNextWords
import markov.buildWordList
import markov.generateText
import snowflake.makeSnowflake
import vote.holdAlternativeVote

/** A short source text with enough repetition for the Markov chain to branch. */
private const val SAMPLE_TEXT = """
    The tide came in. The tide went out. The gulls did not care either way.
    A boat came in. A boat went out. The harbour stayed exactly where it was.
"""

/**
 * Run a small demonstration of each of the three ported programs.
 *
 * The output uses a fixed random seed so that repeated runs agree.
 */
fun main() {
    val random = Random(seed = 2026)

    println("--- Markov text generation ---")
    val nextWords = buildNextWords(buildWordList(SAMPLE_TEXT))
    println("Distinct words tracked: ${nextWords.size}")
    println(generateText(nextWords, numSentences = 3, random = random))

    println()
    println("--- Instant runoff election ---")
    val candidates = listOf("Memphis", "Nashville", "Chattanooga", "Knoxville")
    val votes = buildList {
        repeat(42) { add(listOf("Memphis", "Nashville", "Chattanooga", "Knoxville")) }
        repeat(26) { add(listOf("Nashville", "Chattanooga", "Knoxville", "Memphis")) }
        repeat(15) { add(listOf("Chattanooga", "Knoxville", "Nashville", "Memphis")) }
        repeat(17) { add(listOf("Knoxville", "Chattanooga", "Nashville", "Memphis")) }
    }
    val result = holdAlternativeVote(candidates, votes)
    println("Winner: ${result.winner} with ${result.votes} votes")

    println()
    println("--- Koch snowflake ---")
    val triangle = listOf(
        Point(0.0, 0.0),
        Point(1.0, 0.0),
        Point(0.5, -0.8660254037844386),
        Point(0.0, 0.0),
    )
    for (depth in 0..5) {
        println("depth $depth: ${makeSnowflake(triangle, depth).size} points")
    }
}
