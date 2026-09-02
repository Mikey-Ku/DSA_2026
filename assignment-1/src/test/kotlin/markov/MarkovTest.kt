package markov

import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertTrue

/**
 * A source text paired with the next-word map it should produce.
 *
 * @property description What the case is checking, used in failure messages.
 * @property sourceText The raw text to feed through the pipeline.
 * @property expected The map [buildNextWords] should return for it.
 */
private data class NextWordsCase(
    val description: String,
    val sourceText: String,
    val expected: Map<String, List<String>>,
)

/** Count how many times each element appears, so list order does not matter. */
private fun <T> List<T>.multiset(): Map<T, Int> = groupingBy { it }.eachCount()

/**
 * Single sentences made only of distinct words.
 *
 * Because no word ever has a choice of successor, generating from one of these
 * has exactly one possible outcome: the original sentence. That makes them
 * usable for testing a random process without depending on the random seed.
 */
private val NONREPEATING_CASES = listOf(
    NextWordsCase(
        "a plain sentence",
        "Call me Ishmael.",
        mapOf("" to listOf("Call"), "Call" to listOf("me"), "me" to listOf("Ishmael."), "Ishmael." to listOf("")),
    ),
    NextWordsCase(
        "a punctuation-only word mid-sentence",
        "I - wait, what?",
        mapOf("" to listOf("I"), "I" to listOf("-"), "-" to listOf("wait,"), "wait," to listOf("what?"), "what?" to listOf("")),
    ),
    NextWordsCase(
        "words repeated but with differing case or punctuation",
        "You are what you are.",
        mapOf(
            "" to listOf("You"), "You" to listOf("are"), "are" to listOf("what"),
            "what" to listOf("you"), "you" to listOf("are."), "are." to listOf(""),
        ),
    ),
    NextWordsCase(
        "punctuation in the middle of a word",
        "Just type example.com into your browser!",
        mapOf(
            "" to listOf("Just"), "Just" to listOf("type"), "type" to listOf("example.com"),
            "example.com" to listOf("into"), "into" to listOf("your"),
            "your" to listOf("browser!"), "browser!" to listOf(""),
        ),
    ),
)

/** Cases that stress how whitespace is collapsed. */
private val SPACING_CASES = listOf(
    NextWordsCase(
        "repeated sentences across newlines",
        "I am Sam.\n\nI am Sam.\nSam I am.",
        mapOf(
            "" to listOf("I", "I", "Sam"),
            "I" to listOf("am", "am", "am."),
            "am" to listOf("Sam.", "Sam."),
            "Sam." to listOf(""),
            "Sam" to listOf("I"),
            "am." to listOf(""),
        ),
    ),
    NextWordsCase(
        "a single word",
        "Hippopotomonstrosesquipedaliophobia.",
        mapOf(
            "" to listOf("Hippopotomonstrosesquipedaliophobia."),
            "Hippopotomonstrosesquipedaliophobia." to listOf(""),
        ),
    ),
    NextWordsCase(
        "many consecutive newlines",
        "Hi!\n\n\n\n\n\n\n\n\n\n\n\n...anyone there?",
        mapOf(
            "" to listOf("Hi!", "...anyone"),
            "Hi!" to listOf(""),
            "...anyone" to listOf("there?"),
            "there?" to listOf(""),
        ),
    ),
    NextWordsCase(
        "leading and trailing whitespace, ending mid-sentence",
        "    INT. KITCHEN - CONTINUOUS       ",
        mapOf(
            "" to listOf("INT.", "KITCHEN"),
            "INT." to listOf(""),
            "KITCHEN" to listOf("-"),
            "-" to listOf("CONTINUOUS"),
        ),
    ),
    NextWordsCase(
        "leading and trailing newlines",
        "\nWait, is this the first line?\n",
        mapOf(
            "" to listOf("Wait,"), "Wait," to listOf("is"), "is" to listOf("this"),
            "this" to listOf("the"), "the" to listOf("first"),
            "first" to listOf("line?"), "line?" to listOf(""),
        ),
    ),
    NextWordsCase(
        "two spaces after a sentence",
        "Hello, I'm Microsoft Word.  Since April 2020, two spaces after a sentence is considered an error.",
        mapOf(
            "" to listOf("Hello,", "Since"),
            "Hello," to listOf("I'm"), "I'm" to listOf("Microsoft"),
            "Microsoft" to listOf("Word."), "Word." to listOf(""),
            "Since" to listOf("April"), "April" to listOf("2020,"),
            "2020," to listOf("two"), "two" to listOf("spaces"),
            "spaces" to listOf("after"), "after" to listOf("a"),
            "a" to listOf("sentence"), "sentence" to listOf("is"),
            "is" to listOf("considered"), "considered" to listOf("an"),
            "an" to listOf("error."), "error." to listOf(""),
        ),
    ),
)

/** Cases where words genuinely branch, so repetition in the lists matters. */
private val BRANCHING_CASES = listOf(
    NextWordsCase(
        "one word followed by different words",
        "Arlington Boston Arlington Cambridge.",
        mapOf(
            "" to listOf("Arlington"),
            "Arlington" to listOf("Boston", "Cambridge."),
            "Boston" to listOf("Arlington"),
            "Cambridge." to listOf(""),
        ),
    ),
    NextWordsCase(
        "several possible starting words",
        "Raindrops. Roses. Whiskers on kittens.",
        mapOf(
            "" to listOf("Raindrops.", "Roses.", "Whiskers"),
            "Raindrops." to listOf(""),
            "Roses." to listOf(""),
            "Whiskers" to listOf("on"),
            "on" to listOf("kittens."),
            "kittens." to listOf(""),
        ),
    ),
    NextWordsCase(
        "heavily repeated word sequences",
        "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo.",
        mapOf(
            "" to listOf("Buffalo"),
            "Buffalo" to listOf("buffalo", "buffalo", "buffalo."),
            "buffalo" to listOf("Buffalo", "buffalo", "buffalo", "Buffalo"),
            "buffalo." to listOf(""),
        ),
    ),
)

private val ALL_CASES = SPACING_CASES + NONREPEATING_CASES + BRANCHING_CASES

class BuildWordListTest {
    @Test
    fun `splitting matches a plain whitespace split for every case`() {
        for (case in ALL_CASES) {
            assertEquals(
                case.sourceText.trim().split(Regex("\\s+")),
                buildWordList(case.sourceText),
                case.description,
            )
        }
    }

    @Test
    fun `runs of whitespace collapse and never produce empty words`() {
        assertEquals(listOf("a", "b", "c"), buildWordList("  a \t\n b     c \n "))
    }

    @Test
    fun `text with no words yields no words`() {
        assertEquals(emptyList(), buildWordList(""))
        assertEquals(emptyList(), buildWordList("   \n\t  "))
    }
}

class BuildNextWordsTest {
    @Test
    fun `every case produces the expected next-word map`() {
        for (case in ALL_CASES) {
            val actual = buildNextWords(buildWordList(case.sourceText))

            assertEquals(
                case.expected.keys,
                actual.keys,
                "${case.description}: wrong set of words tracked",
            )
            for ((word, expectedNext) in case.expected) {
                // Order within a word's list carries no meaning, but how many
                // times each successor appears does, so compare as multisets.
                assertEquals(
                    expectedNext.multiset(),
                    actual.getValue(word).multiset(),
                    "${case.description}: wrong successors for \"$word\"",
                )
            }
        }
    }

    @Test
    fun `a word that ends a sentence is only ever followed by the boundary`() {
        for (case in ALL_CASES) {
            val actual = buildNextWords(buildWordList(case.sourceText))
            for ((word, nextWords) in actual) {
                if (word.isNotEmpty() && word.last() in ".!?") {
                    assertEquals(
                        listOf(SENTENCE_BOUNDARY),
                        nextWords,
                        "${case.description}: \"$word\" ends a sentence",
                    )
                }
            }
        }
    }

    @Test
    fun `an empty text tracks only an unreachable boundary`() {
        // An empty text still records the boundary, with nothing following it,
        // so no sentence can be generated from the result.
        assertEquals(mapOf(SENTENCE_BOUNDARY to emptyList()), buildNextWords(emptyList()))
    }

    @Test
    fun `a text that stops mid-sentence drops its dangling final word`() {
        assertEquals(
            mapOf(SENTENCE_BOUNDARY to listOf("hello")),
            buildNextWords(buildWordList("hello")),
        )
    }

    @Test
    fun `the boundary never lists itself as a successor`() {
        for (case in ALL_CASES) {
            val actual = buildNextWords(buildWordList(case.sourceText))
            assertTrue(
                SENTENCE_BOUNDARY !in actual[SENTENCE_BOUNDARY].orEmpty(),
                "${case.description}: an empty sentence could be generated",
            )
        }
    }
}

class GenerateSentenceTest {
    @Test
    fun `a source with no branching regenerates itself exactly`() {
        for (case in NONREPEATING_CASES) {
            val nextWords = buildNextWords(buildWordList(case.sourceText))
            assertEquals(case.sourceText, generateSentence(nextWords), case.description)
        }
    }

    @Test
    fun `the same seed always produces the same sentence`() {
        val nextWords = buildNextWords(buildWordList(BRANCHING_CASES[2].sourceText))
        val first = generateSentence(nextWords, Random(seed = 42))
        val second = generateSentence(nextWords, Random(seed = 42))
        assertEquals(first, second)
    }

    @Test
    fun `different seeds explore different sentences`() {
        val nextWords = buildNextWords(buildWordList(BRANCHING_CASES[2].sourceText))
        val sentences = (1..50).map { generateSentence(nextWords, Random(seed = it)) }.toSet()
        assertTrue(sentences.size > 1, "every seed produced the same sentence: $sentences")
    }

    @Test
    fun `generated sentences always end a sentence and never start with a space`() {
        val nextWords = buildNextWords(buildWordList(BRANCHING_CASES[1].sourceText))
        for (seed in 1..50) {
            val sentence = generateSentence(nextWords, Random(seed))
            assertTrue(sentence.last() in ".!?", "seed $seed produced \"$sentence\"")
            assertTrue(sentence.first() != ' ', "seed $seed produced \"$sentence\"")
        }
    }

    @Test
    fun `a word with no recorded successors is reported rather than crashing obscurely`() {
        assertFailsWith<IllegalArgumentException> {
            generateSentence(mapOf(SENTENCE_BOUNDARY to listOf("dangling")))
        }
    }
}

class GenerateTextTest {
    @Test
    fun `a source with no branching repeats itself the requested number of times`() {
        for (case in NONREPEATING_CASES) {
            val nextWords = buildNextWords(buildWordList(case.sourceText))
            for (numSentences in 1..3) {
                assertEquals(
                    List(numSentences) { case.sourceText }.joinToString(" "),
                    generateText(nextWords, numSentences),
                    "${case.description} (x$numSentences)",
                )
            }
        }
    }

    @Test
    fun `asking for no sentences produces an empty string`() {
        val nextWords = buildNextWords(buildWordList("Call me Ishmael."))
        assertEquals("", generateText(nextWords, 0))
    }

    @Test
    fun `a negative sentence count is rejected`() {
        val nextWords = buildNextWords(buildWordList("Call me Ishmael."))
        assertFailsWith<IllegalArgumentException> { generateText(nextWords, -1) }
    }
}
