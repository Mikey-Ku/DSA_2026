package translation

// Use a Markov process to generate random sentences based on a source text.

import kotlin.random.Random

/** The marker used for the start or end of a sentence. */
const val SENTENCE_BOUNDARY: String = ""

/** The characters that, at the end of a word, end a sentence. */
private const val TERMINATORS = ".!?"

/** Matches any run of whitespace. */
private val WHITESPACE = Regex("\\s+")

/**
 * Report whether a word ends a sentence.
 *
 * @param word The word to check.
 * @return `true` if [word] is non-empty and ends in `.`, `!`, or `?`.
 */
private fun endsSentence(word: String): Boolean =
    word.isNotEmpty() && word.last() in TERMINATORS

/**
 * Take in a string of text and return a list of strings that represents the
 * original string separated by every whitespace.
 *
 * @param sourceText String of text the user wants to separate.
 * @return A list of strings that represents the string of text separated into
 *     individual words.
 */
fun buildWordList(sourceText: String): List<String> =
    sourceText.split(WHITESPACE).filter { it.isNotEmpty() }

/**
 * Take in the separated string list and create a map that has each string as a
 * key and a list corresponding to each key that represents the strings that
 * could possibly follow it.
 *
 * @param wordList List of strings that represent the separated words.
 * @return A map of each separated string as a key and the possible strings that
 *     could follow it as its values.
 */
fun buildNextWords(wordList: List<String>): Map<String, List<String>> {
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
            nextWords.getOrPut(current) { mutableListOf(SENTENCE_BOUNDARY) }
        } else {
            nextWords.getOrPut(current) { mutableListOf() }.add(next)
        }
    }

    if (tokens.last() == tokens[tokens.size - 2]) {
        nextWords[SENTENCE_BOUNDARY]?.remove(SENTENCE_BOUNDARY)
    }

    val lastWord = tokens[tokens.size - 2]
    if (lastWord != SENTENCE_BOUNDARY) {
        nextWords.remove(lastWord)
    }

    return nextWords
}

/**
 * Take in a map of words and produce a randomly generated sentence, using the
 * previous word's values to generate the next word.
 *
 * @param nextWords Map of words (keys) and possible words that follow (values).
 * @param random The source of randomness. Defaults to the shared generator.
 * @return A randomly generated sentence compiled from the map of words and their
 *     possible values.
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
 * Take in a map of words and produce as many randomly generated sentences as
 * [numSentences].
 *
 * @param nextWords A map of strings as keys and their values as a list of
 *     possible strings that can follow.
 * @param numSentences The number of sentences the user would like to output.
 * @param random The source of randomness. Defaults to the shared generator.
 * @return A string that is [numSentences] sentences long and is a combination of
 *     the randomly generated strings using the [nextWords] map.
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
