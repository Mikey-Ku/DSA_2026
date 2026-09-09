package translation

import kotlin.random.Random

/**
 * The marker used for "the start or end of a sentence".
 *
 * It is deliberately the empty string, which is a value [buildWordList] can
 * never produce, so it cannot collide with a real word.
 */
const val SENTENCE_BOUNDARY: String = ""

/** The characters that, at the end of a word, end a sentence. */
private const val TERMINATORS = ".!?"

/** Matches any run of whitespace, so consecutive spaces and newlines split as one. */
private val WHITESPACE = Regex("\\s+")

/**
 * Report whether a word ends a sentence.
 *
 * @param word The word to check.
 * @return `true` if [word] is non-empty and its last character is `.`, `!`, or `?`.
 */
private fun endsSentence(word: String): Boolean =
    word.isNotEmpty() && word.last() in TERMINATORS

/**
 * Split a source text into words.
 *
 * Any run of whitespace separates words, and leading and trailing whitespace is
 * ignored, so no empty strings appear in the result.
 *
 * @param sourceText The text to split.
 * @return The words of [sourceText], in order.
 */
fun buildWordList(sourceText: String): List<String> =
    sourceText.split(WHITESPACE).filter { it.isNotEmpty() }

/**
 * Build the map of which words can follow which other words.
 *
 * [SENTENCE_BOUNDARY] is used as a pseudo-word on both ends of every sentence,
 * so the words mapped to it are exactly the words that can start a sentence, and
 * every sentence-ending word maps to it and nothing else.
 *
 * Repetition is meaningful: if a word is followed by "the" three times and by
 * "a" once, "the" appears three times in its list. That is what weights the
 * random choice in [generateSentence] toward the more common continuation.
 *
 * @param wordList The words of a source text, in order, as produced by
 *     [buildWordList].
 * @return A map from each word to the list of words that may follow it.
 */
fun buildNextWords(wordList: List<String>): Map<String, List<String>> {
    // Wrap the text in sentence boundaries, and slot another boundary in after
    // every word that ends a sentence. Walking consecutive pairs of this list
    // then yields every transition the text contains.
    val tokens = buildList {
        add(SENTENCE_BOUNDARY)
        for (word in wordList) {
            add(word)
            if (endsSentence(word)) {
                add(SENTENCE_BOUNDARY)
            }
        }
        add(SENTENCE_BOUNDARY)
    }

    val nextWords = LinkedHashMap<String, MutableList<String>>()
    for (index in 0 until tokens.size - 1) {
        val current = tokens[index]
        val next = tokens[index + 1]
        if (endsSentence(current)) {
            // A word that ends a sentence can only ever be followed by the
            // boundary, so record that once and ignore later repeats.
            nextWords.getOrPut(current) { mutableListOf(SENTENCE_BOUNDARY) }
        } else {
            nextWords.getOrPut(current) { mutableListOf() }.add(next)
        }
    }

    // If the text already ended a sentence, the closing boundary added above is
    // one too many and shows up as a spurious boundary-to-boundary transition.
    if (tokens.last() == tokens[tokens.size - 2]) {
        nextWords[SENTENCE_BOUNDARY]?.remove(SENTENCE_BOUNDARY)
    }

    // A text that stops mid-sentence leaves its final word with no recorded
    // continuation, so drop it rather than leave a dead end that would strand
    // sentence generation.
    val lastWord = tokens[tokens.size - 2]
    if (lastWord != SENTENCE_BOUNDARY) {
        nextWords.remove(lastWord)
    }

    return nextWords
}

/**
 * Generate one random sentence from a map of next words.
 *
 * Starting from [SENTENCE_BOUNDARY], a next word is chosen at random until one
 * of them ends a sentence.
 *
 * The source of randomness is a parameter rather than a global, so a caller can
 * pass a seeded [Random] and get repeatable output.
 *
 * @param nextWords A map from each word to the words that may follow it, as
 *     produced by [buildNextWords].
 * @param random The source of randomness. Defaults to the shared generator.
 * @return A randomly generated sentence.
 * @throws IllegalArgumentException If generation reaches a word that [nextWords]
 *     has no entry for.
 */
fun generateSentence(
    nextWords: Map<String, List<String>>,
    random: Random = Random.Default,
): String {
    val sentence = StringBuilder()
    var previousWord = SENTENCE_BOUNDARY

    while (true) {
        val possibleWords = requireNotNull(nextWords[previousWord]) {
            "No next words recorded for \"$previousWord\"."
        }
        val nextWord = possibleWords.random(random)

        if (endsSentence(nextWord)) {
            return sentence.append(nextWord).toString()
        }
        sentence.append(nextWord).append(' ')
        previousWord = nextWord
    }
}

/**
 * Generate several random sentences, joined by single spaces.
 *
 * @param nextWords A map from each word to the words that may follow it, as
 *     produced by [buildNextWords].
 * @param numSentences How many sentences to generate. Must not be negative.
 * @param random The source of randomness. Defaults to the shared generator.
 * @return [numSentences] randomly generated sentences separated by spaces, or an
 *     empty string if [numSentences] is zero.
 * @throws IllegalArgumentException If [numSentences] is negative.
 */
fun generateText(
    nextWords: Map<String, List<String>>,
    numSentences: Int,
    random: Random = Random.Default,
): String {
    require(numSentences >= 0) {
        "Cannot generate a negative number of sentences, but asked for $numSentences."
    }
    return (0 until numSentences).joinToString(" ") { generateSentence(nextWords, random) }
}
