# Assignment 1: Hello World and Getting to Know You

Michael Ku
Data Structures and Algorithms, Fall 2026

## Part 1: Course Entry Survey

Submitted through the Google Form. Nothing in this repo.

## Part 2: Identifying Effective Strategies for Learning

### 1. Choose a moment in your educational career where learning went really well. What strategies did you use that worked particularly well?

**Answer:**


### 2. Which strategies have led to less effective learning, or less enjoyment of the learning experience?

**Answer:**


### 3. The instructor's view is that grappling with a problem is what makes the concepts stick, and that prompting an AI for answers and copying them does not get you there. Do you agree with this framing? How are you thinking about AI tools in this course?

**Answer:**


### 4. What strategies will you use in this course to be successful? With respect to AI, what principles will you use?

**Answer:**


### 5. What do you think of the proposed activities for the oral quizzes? Would you add or subtract any?

**Answer:**


### 6. How can the teaching team support you?

**Answer:**


---

## Part 3: Hello World

I read the *Getting Set with Kotlin* page and worked through the beginner Kotlin
tour, attempting the exercises.

### 1. What features do you like about Kotlin?

**Answer:**


### 2. Are there things you were expecting to find that you haven't?

**Answer:**


### 3. What questions do you have?

**Answer:**


### 4. Did you use the debugger? Do you have experience with interactive debuggers? Were you able to launch it?

**Answer:**


---

## Part 4: Translating Your Old Code

### What the original code was

Three Python programs I wrote for the dictionaries, recursion, and refactoring
assignment for Softdes 2025:

1. **Markov text generation.** Reads a source text, records which words follow
   which other words, and generates new sentences by walking that record at
   random. Repetition is kept, so a word seen three times after "the" is three
   times as likely to be chosen.
2. **Instant-runoff voting.** Runs an alternative-vote election. Each round every
   ballot counts for its highest-ranked candidate still in the race. A candidate
   with an absolute majority wins; otherwise the last-placed candidate is
   eliminated and the round repeats.
3. **Koch snowflake.** Replaces every line segment with four segments a third as
   long, with an equilateral bump on the middle third, and repeats.

### The Kotlin code

| File | Contents |
| --- | --- |
| `src/main/kotlin/markov/Markov.kt` | `buildWordList`, `buildNextWords`, `generateSentence`, `generateText` |
| `src/main/kotlin/vote/Vote.kt` | `tallyVotes`, `getMinimumCandidate`, `holdAlternativeVote` (recursive), `holdIterativeVote` (the original loop) |
| `src/main/kotlin/snowflake/Snowflake.kt` | `transformSegment`, `makeSnowflake` |
| `src/main/kotlin/geometry/Geometry.kt` | `Point`, `dist`, `degrees`, `addDistDegrees` |
| `src/main/kotlin/Main.kt` | Demo runner for all four programs |

### Tests

62 tests for this part, in `src/test/kotlin/{markov,vote,snowflake,geometry}/`.
Most cases come from the original pytest suites so the port is held to the same
contract. A few are new, and were only possible because the random generator is
now injected: that the same seed reproduces a sentence, and that different seeds
produce different ones.

The Python I translated from is kept in `reference/python/` so the original and
the port can be read side by side.

### How the translation went

Short version: `tailrec` made the recursive rewrite better than the loop it
replaced instead of worse, data classes fixed the untyped tuples, and injecting
the random generator made the text generator testable. The awkward parts were
Python's `str.split()` having no Kotlin equivalent, a loop in the original that
mutates the list it iterates over, and a condition in the original that turns out
to have no effect.

Full writeup, including the parts that went badly:
**[docs/translation-writeup.md](docs/translation-writeup.md)**

---

## Part 5: Implementing Meeting Scheduler

Determines whether a collection of meetings contains a conflict. Meetings are
half-open intervals `[start, end)`, so a meeting ending exactly when another
begins is not a conflict.

Both required algorithms are in `src/main/kotlin/scheduler/Scheduler.kt`:

- `findConflictByPairs` — the straightforward version, comparing every pair
- `findConflictBySorting` — sorts by start time with Kotlin's built-in
  `sortedBy`, then compares only neighbouring meetings

Expected growth with n:

| | Best case | Worst case | Extra space |
| --- | --- | --- | --- |
| Pairwise | O(1) | Θ(n²) | O(1) |
| Sort first | Θ(n log n) | Θ(n log n) | O(n) |

Doubling n should roughly quadruple the pairwise time. The sorting version is
Θ(n log n) in every case, because the sort runs before anything can return early.

21 tests in `src/test/kotlin/scheduler/SchedulerTest.kt` cover both
implementations, including both examples from the day 1 page, the edge case of
one meeting ending exactly when another starts, and 2000 randomly generated
schedules checking that the two algorithms always agree.

Writeup, including why comparing only neighbours is enough and measured timings
against the predicted growth:
**[docs/meeting-scheduler.md](docs/meeting-scheduler.md)**

---

## Layout

```
assignment-1/
├── README.md                        this file
├── build.gradle.kts
├── docs/
│   ├── translation-writeup.md       part 4 writeup
│   └── meeting-scheduler.md         part 5 writeup
├── src/main/kotlin/
│   ├── Main.kt
│   ├── geometry/Geometry.kt
│   ├── markov/Markov.kt
│   ├── vote/Vote.kt
│   ├── snowflake/Snowflake.kt
│   └── scheduler/
│       ├── Scheduler.kt
│       └── Benchmark.kt
├── src/test/kotlin/                 83 tests
└── reference/python/                the original Python, unmodified
```
