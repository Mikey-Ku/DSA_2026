# Hello World! — Kotlin Tour

> **Your answers go here, in your own words.** The questions below are about your
> experience going through the tour, so they need you to have actually gone
> through it. Delete this block before submitting.

Confirm for the instructor: did you finish the [beginner Kotlin
tour](https://kotlinlang.org/docs/kotlin-tour-welcome.html), attempting all the
exercises?

_Your answer:_

## 1. What features do you like about Kotlin?

_Your answer:_

## 2. Are there things you were expecting to find that you haven't?

_Your answer:_

## 3. What questions do you have?

_Your answer:_

## 4. The debugger

Try using the debugger. Do you have experience using interactive debuggers like
this one? Were you able to successfully launch it?

> **Setup note.** The course's *Getting Set with Kotlin* page describes the
> debugger in IntelliJ IDEA terms — breakpoints as red circles in the gutter, the
> bug icon next to the run arrow, a variables pane, a resume button. **VS Code
> with only the `mathiasfrohlich.kotlin` extension cannot debug Kotlin at all**:
> that extension is a syntax grammar with no language server and no debug
> adapter. To answer this question you will need IntelliJ IDEA Community Edition
> (free), which is what the course page assumes.

_Your answer:_

---

## Raw material from this assignment

Not answers — just Kotlin features this assignment actually made you use, in case
they are useful when writing the above. Every one of these appears in the code in
this folder.

- **`tailrec`** — `makeSnowflake` and `holdAlternativeVote` are compiled to loops
  rather than recursion, so they survive depths that crash the Python originals.
- **`data class`** — `Point`, `Meeting`, `ElectionResult`, `Conflict`. Generated
  `equals`/`toString` are what make the test failure messages readable.
- **Null safety** — `getMinimumCandidate` returns `String?`, and
  `findConflictByPairs` returns `Conflict?`. The compiler forces the empty case
  to be handled rather than leaving it to blow up later.
- **Default and named arguments** — `generateSentence(nextWords, random = ...)`,
  which is what made the random generator injectable and the tests deterministic.
- **`List` vs `MutableList` as distinct types** — read-only by default, mutation
  opted into.
- **`require` / `requireNotNull`** — argument validation that fails loudly at the
  call site instead of somewhere deep inside a loop.
- **Backtick test names** — `` fun `a meeting ending exactly when another begins
  is not a conflict`() ``, which reads as a sentence in the test report.
- **Expression bodies and trailing lambdas** — `sortedBy { it.start }`,
  `meetings.count { winner in it }`.
- **Destructuring** — `val (_, oneThird, peak, twoThirds, _) = transformSegment(...)`.

Things Kotlin made you go outside the standard library for, which may be worth
raising under question 2 or 3:

- No `toDegrees` / `toRadians` in `kotlin.math` — `geometry/Geometry.kt` falls
  back to `Math.toDegrees` from the JVM.
- No equivalent of Python's `str.split()` with no argument, which splits on runs
  of whitespace; `Markov.kt` uses `split(Regex("\\s+")).filter { it.isNotEmpty() }`.
- No `assertClose` for floating-point comparison in `kotlin.test`;
  `GeometryTest.kt` defines its own.
