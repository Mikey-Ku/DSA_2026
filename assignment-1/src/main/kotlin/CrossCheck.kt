import java.io.File
import markov.buildNextWords
import markov.buildWordList

/**
 * Decode the `\n`, `\t`, and `\\` escapes used in the shared corpus file.
 *
 * @param line A single raw line from the corpus.
 * @return The source text the line represents.
 */
private fun unescape(line: String): String {
    val result = StringBuilder(line.length)
    var index = 0
    while (index < line.length) {
        if (line[index] == '\\' && index + 1 < line.length) {
            when (val escape = line[index + 1]) {
                'n' -> result.append('\n')
                't' -> result.append('\t')
                '\\' -> result.append('\\')
                else -> result.append('\\').append(escape)
            }
            index += 2
        } else {
            result.append(line[index])
            index += 1
        }
    }
    return result.toString()
}

/**
 * Print the next-word map this port builds for each line of a corpus.
 *
 * The output format matches `reference/python/crosscheck.py` exactly, so the two
 * can be diffed to show that the Kotlin translation and the Python original
 * agree on real inputs.
 *
 * @param args A single argument: the path to the corpus file.
 */
fun main(args: Array<String>) {
    require(args.size == 1) { "Usage: crossCheck <corpus-file>" }

    File(args[0]).readText().split("\n").forEachIndexed { caseNumber, rawLine ->
        if (rawLine.isEmpty()) return@forEachIndexed
        val nextWords = buildNextWords(buildWordList(unescape(rawLine)))
        for (word in nextWords.keys.sorted()) {
            val successors = nextWords.getValue(word).sorted().joinToString("|")
            println("$caseNumber\t$word\t$successors")
        }
    }
}
