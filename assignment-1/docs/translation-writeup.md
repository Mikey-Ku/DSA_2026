# Translating Your Old Code

Part 4 of assignment 1. See [the assignment README](../README.md) for the other parts.

A Kotlin port of three Python programs I wrote for Olin's Software Design
course, plus the tests and tooling to show the translation preserved their
behaviour.

- **Original language:** Python 3 (with type hints on the provided helpers)
- **Target language:** Kotlin 2.4, JVM toolchain 21, built with Gradle
- **Tests:** 62 for this part (83 across the whole assignment), `kotlin.test` on JUnit 5
- **External libraries:** none beyond the test framework

---

## What the code does

The source was one assignment, *dictionaries, recursion, and refactoring*,
made up of three unrelated programs. All three are ported here.

### 1. Markov text generation (`markov`)

Reads a source text and learns which words can follow which other words, then
generates new sentences by walking that map at random. The core data structure
is a map from each word to a **list** (not a set) of the words observed after
it, so a word that follows three times appears three times and is three times as
likely to be picked. The empty string does duty as a sentence-boundary marker on
both ends of every sentence, which is what lets the generator know where a
sentence can start and where it must stop.

This is the "dictionaries" half of the assignment.

### 2. Instant-runoff voting (`vote`)

Runs an alternative-vote election. Each round, every ballot counts for its
highest-ranked candidate still in the race. If somebody holds an absolute
majority of the votes cast, they win; otherwise the candidate with the fewest
votes is eliminated and the election runs again with the rest. Ballots need not
rank every candidate, so once all the candidates a ballot names are eliminated
it stops counting toward the total.

The assignment supplied a working iterative implementation and asked for a
recursive rewrite, which is the "refactoring" half. **Both versions are ported**
(`holdIterativeVote` and `holdAlternativeVote`), because the whole point of that
exercise was that they must agree, and that is a property worth asserting
rather than assuming. See `RefactoringEquivalenceTest`.

### 3. Koch snowflake (`snowflake`, `geometry`)

Generates the points of a Koch snowflake. Each line segment is replaced by four
segments a third as long, with an equilateral bump pushed out counterclockwise
from the middle third, and the process repeats. This is the "recursion" half.

The Python original imported matplotlib to draw the result. The port keeps the
three geometry helpers it actually needed (`dist`, `degrees`, `addDistDegrees`)
and drops the plotting, which is why this project has no third-party
dependencies at all.

---

## Running it

See [the assignment README](../README.md) for the commands. The Python this was
translated from is in `reference/python/`, unmodified, so the two can be read
side by side.

## Writeup: how the translation went

### The good

**`tailrec` turned recursion into a real tool rather than a liability.** Both
`makeSnowflake` and `holdAlternativeVote` are tail-recursive, and marking them
`tailrec` makes the compiler rewrite them as loops. This is not a theoretical
nicety. There is a test that runs `makeSnowflake` at a depth of **1,000,000**
and one that runs an election with **3,000 candidates**, eliminating one per
round; both pass. The Python originals are written exactly the same way and
would hit the interpreter's default recursion limit at around 1,000 frames. The
recursive version of the vote function was the assignment's *refactoring*
exercise, and in Python it is strictly worse than the loop it replaced, since it can
only handle smaller elections. In Kotlin it costs nothing. That was the single
most satisfying thing I found.

**Data classes made tuples honest.** Both programs leaned on tuples: points were
`tuple[float, float]`, and the election returned a bare `(str, int)`. That alias
is erased at runtime, so nothing stops a three-element tuple from flowing
through the snowflake code until it fails somewhere far from the mistake, and
every caller of the vote function had to remember which slot was which.
`data class Point(val x: Double, val y: Double)` and
`data class ElectionResult(val winner: String, val votes: Int)` fixed both, and
the generated `equals`/`toString` paid for themselves in the tests. A whole
snowflake can be compared with one `assertEquals`, and a failure prints readable
points instead of a wall of unlabelled numbers.

**Passing the randomness in was the biggest testability win.** The Python called
`random.choice`, which reads the interpreter-wide generator. The only way to
make its output repeatable is `random.seed()`, which mutates process-global state
and can be clobbered by anything else in the test run. The original test suite
sidesteps this entirely by only ever testing sentences with no branching, where
the random choice has nothing to choose between. In Kotlin I made it a parameter
with a default:

```kotlin
fun generateSentence(nextWords: Map<String, List<String>>, random: Random = Random.Default): String
```

Callers who don't care are unaffected; tests pass `Random(seed = 42)` and get
determinism with no global state. That let me write tests the original couldn't:
that the same seed reproduces a sentence, that different seeds actually explore
different sentences, and that every generated sentence ends in terminal
punctuation, on a genuinely branching source text.

**`List` and `MutableList` being different types forced me to be deliberate.**
In Python every list is mutable and you find out at runtime. Having to write
`Map<String, List<String>>` on the way out but `LinkedHashMap<String,
MutableList<String>>` on the way in made it obvious which structures were still
under construction and which were finished.

### The bad

**Python's `str.split()` is not `split(" ")`, and that is a real trap.** Called
with no argument it splits on *runs* of whitespace and discards leading and
trailing whitespace. Kotlin's `String.split` has no equivalent overload, and the
obvious translation, `sourceText.split(" ")`, silently produces empty strings
for every double space and newline, which then become fake words in the map and
poison everything downstream. The correct translation is
`sourceText.split(Regex("\\s+")).filter { it.isNotEmpty() }`. The original test
suite has six separate cases about whitespace, which is how I knew to look.

**Ceremony.** The Python was four files in a folder. Getting Kotlin to the point
of running one line of it meant a Gradle build script, a settings file, a
toolchain declaration, and a wrapper. My system `java` was 11, which Gradle
9 refuses to run on, so that had to be sorted before anything compiled at all.
Once it was working the tooling was genuinely better (a real test runner, a
compiler that catches typos), but the distance from zero to *hello world* is
much longer.

**`kotlin.math` has no degree conversion.** There is no `toDegrees`/`toRadians`
in the Kotlin standard library, so `geometry` calls `Math.toDegrees` and
`Math.toRadians` from the JVM. It works fine, but it is a reminder that Kotlin's
stdlib is deliberately thin and leans on Java underneath.

**Float comparison had to be rebuilt.** Python's `math.isclose(a, b,
abs_tol=1e-9)` has no `kotlin.test` equivalent, so the geometry tests define
`assertClose` and `assertPointClose`. The absolute tolerance matters here, because many
of the coordinates under test are very near zero, where a relative comparison
behaves badly.

### The ugly

**`build_next_words` mutates the list it is iterating over.** The original walks
`words` with a `while i < len(words) - 1` loop and calls `words.insert(i + 1,
"")` inside the loop body, growing the list whose length is the loop bound,
while the index walks forward into the thing it just inserted. It works, but I
could not port it until I could state what it was actually doing. It turns out
to be equivalent to something much simpler: insert a boundary marker after every
sentence-ending word *up front*, then walk consecutive pairs. The Kotlin does
that, and produces byte-identical output on every input I have thrown at it. The
translation didn't just move the code, it forced me to understand it, and the
result is shorter and has no mutation-during-iteration at all.

**I found a condition that does nothing.** The original ends with:

```python
if punctuation not in last_word and last_word != "":
    del word_dict[last_word]
```

`punctuation` is the string `".!?"`, so `punctuation not in last_word` is a
*substring* test. It asks whether the word literally contains the three
characters `.!?` in a row. It was surely meant to be `last_word[-1] not in
punctuation`, testing the final character. The bug never fires: by the time that
line runs, `last_word` is only ever non-empty when the text stopped mid-sentence,
so the first half of the condition is always true and the second half decides
everything. Both the intended version and the written version therefore do the
same thing. I only noticed because translating it meant reading it closely enough
to justify each clause, and one of them couldn't be justified. The Kotlin keeps
only the half that carries meaning, with a comment saying why.

**The empty string wearing three hats.** In the original, `""` is the
start-of-sentence marker, the end-of-sentence marker, and "not a real word",
with nothing naming any of those roles. It is safe, because `build_word_list` can never
produce an empty string, so it cannot collide with real data, but you have to
work that out yourself. The port declares `const val SENTENCE_BOUNDARY = ""` and
says so in a doc comment.

**Failures were silent or obscure; now they aren't.** If the map contained a
dead end, `generate_sentence` died with a bare `KeyError` from inside a `while
True` loop. The port uses `requireNotNull` with a message that names the word it
got stuck on. Similarly `make_snowflake` with a negative depth recurses forever
in Python; the Kotlin rejects it with `require`.

### One thing I decided not to "fix"

Given empty input, the original returns `{"": []}` rather than `{}`, a map with
one key that leads nowhere. It is a harmless artifact of how the sentinels are
laid down. I reproduced it exactly instead of tidying it, and there is a test
that pins it with a comment explaining why. The brief was to translate the code,
not to improve it, and an intentional quirk that is documented and tested is
better than a silent behaviour change. Everywhere I *did* deviate, whether dropping the
matplotlib dependency, injecting the random generator, or adding argument
validation, it was an addition around the edges, not a change to what the
algorithms compute.
