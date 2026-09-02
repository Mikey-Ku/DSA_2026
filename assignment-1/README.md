# Assignment 1 — Hello World and Getting to Know You

Language choice for this course: **Kotlin** (the course default).

## The five parts

| # | Part | Where | Status |
| --- | --- | --- | --- |
| 1 | Course entry survey | [Google Form](https://docs.google.com/forms/d/e/1FAIpQLScJegi7KGH3-TvK7R0ImdSJHRrENx9AuBfAB6pKXzm60bPncw/viewform) | Submitted separately, not in this repo |
| 2 | Identifying effective strategies for learning | [`docs/learning-strategies.md`](docs/learning-strategies.md) | **Needs your answers** |
| 3 | Hello World / Kotlin tour | [`docs/kotlin-tour.md`](docs/kotlin-tour.md) | **Needs your answers** (and the debugger needs IntelliJ) |
| 4 | Translating your old code | [`docs/translation-writeup.md`](docs/translation-writeup.md) | Done — 62 tests |
| 5 | Implementing meeting scheduler | [`docs/meeting-scheduler.md`](docs/meeting-scheduler.md) | Done — 21 tests |

## Building and running

Everything runs **from the repository root**, one level up:

```bash
./gradlew :assignment-1:test        # all 83 unit tests
./gradlew :assignment-1:run         # demo every program
./gradlew :assignment-1:benchmark   # time the two conflict algorithms as n grows
./gradlew :assignment-1:build       # compile and test
```

The Gradle wrapper is checked in and the build declares the JDK it needs, so
none of this depends on which `java` happens to be on `PATH`.

To check the Kotlin port against the Python it came from:

```bash
./assignment-1/reference/crosscheck.sh
```

## What's here

**Part 4 — the port.** Three programs translated from Python, taken from the
dictionaries/recursion/refactoring assignment in Olin's Software Design course:
Markov text generation, instant-runoff voting, and the Koch snowflake. The
writeup covers the good (`tailrec` making recursion viable, data classes
replacing tuples, injecting the random generator), the bad (Python's
whitespace-collapsing `split()`), and the ugly (a loop that mutates the list it
iterates, and a condition in the original that turns out to do nothing).

**Part 5 — the scheduler.** Conflict detection over half-open time intervals,
implemented twice: an O(1)-space Θ(n²) pairwise check and a Θ(n log n) version
that sorts first and compares only neighbours. The writeup proves why comparing
neighbours is sufficient and puts the predicted growth next to measured timings.

## Layout

```
DSA_2026/                            the Gradle build lives at the repo root
├── settings.gradle.kts              declares assignment-1 as a subproject
├── gradlew, gradle/                 wrapper, and the JDK the build asks for
└── assignment-1/
    ├── README.md                    this file
    ├── build.gradle.kts             Kotlin JVM plugin, JVM toolchain 21
    ├── docs/
    │   ├── learning-strategies.md   part 2
    │   ├── kotlin-tour.md           part 3
    │   ├── translation-writeup.md   part 4
    │   └── meeting-scheduler.md     part 5
    ├── src/main/kotlin/
    │   ├── Main.kt                  demo runner
    │   ├── CrossCheck.kt            prints next-word maps for the diff harness
    │   ├── scheduler/Scheduler.kt   meeting conflict detection, both algorithms
    │   ├── scheduler/Benchmark.kt   times the two against each other
    │   ├── markov/Markov.kt         Markov text generation
    │   ├── vote/Vote.kt             instant-runoff voting, recursive + iterative
    │   ├── snowflake/Snowflake.kt   Koch snowflake
    │   └── geometry/Geometry.kt     Point, dist, degrees, addDistDegrees
    ├── src/test/kotlin/             83 tests, one suite per source file
    └── reference/
        ├── corpus.txt               source texts shared by both implementations
        ├── crosscheck.sh            runs the Python and Kotlin, diffs the output
        └── python/                  the original Python, unmodified
```
