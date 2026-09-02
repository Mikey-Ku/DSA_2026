# Meeting Scheduler

Detecting whether a collection of meetings contains a scheduling conflict, two
ways: the straightforward pairwise check, and a faster one that sorts first.

Code: [`src/main/kotlin/scheduler/Scheduler.kt`](../src/main/kotlin/scheduler/Scheduler.kt)
Tests: [`src/test/kotlin/scheduler/SchedulerTest.kt`](../src/test/kotlin/scheduler/SchedulerTest.kt)

## The problem

Given a list of meetings, each with a start and end time, determine whether any
two of them overlap. A meeting ending exactly when another begins does **not**
count as an overlap.

## Modelling the times

A meeting is stored as the half-open interval `[start, end)`, where the end minute is
excluded, with both times held as minutes since midnight.

That single choice is what makes the awkward edge case disappear. Under
half-open intervals, 10:00-11:00 and 11:00-11:30 share no minute, so they simply
are not an overlap; there is no special case to remember and no `if` to get
wrong. Two half-open intervals overlap exactly when

```
a.start < b.end  &&  b.start < a.end
```

Both comparisons are strict. Relaxing either to `<=` would wrongly flag
back-to-back meetings, which is precisely the bug the edge case is testing for.

Times are plain `Int` minutes rather than a date-time type because the problem
lives inside a single day, and integers make the comparisons obvious. `HH:MM`
strings are parsed at the boundary by `timeOf`, so the awkward parsing lives in
one place instead of being scattered through the algorithms.

## Algorithm 1: check every pair

For each meeting, compare it against every meeting later in the list, and return
the first overlapping pair found.

Only *later* meetings are considered. This halves the work and, more usefully,
means a meeting is never compared against itself, which matters, because every
meeting overlaps itself.

**Correctness** is immediate: if a conflicting pair exists, it is one of the
pairs examined.

**Running time.** With no conflict, the loops perform

```
(n-1) + (n-2) + ... + 1  =  n(n-1)/2  comparisons
```

which is Θ(n²). Doubling n should roughly **quadruple** the work. The best case
is O(1). If the first two meetings clash, it returns after one comparison, so
this is Θ(n²) in the worst case, not in every case. Extra space is O(1); the
input is only read.

## Algorithm 2: sort by start time, then check neighbours

Sort the meetings by start time using Kotlin's built-in `sortedBy`, then walk the
sorted list once, comparing only **adjacent** pairs.

The obvious worry is that checking neighbours might miss a conflict between two
meetings that end up far apart after sorting. It cannot, and here is why.

> **Claim.** Let `m₀ … mₙ₋₁` be sorted so that `mᵢ.start ≤ mᵢ₊₁.start`. If any
> two meetings overlap, then some *adjacent* pair overlaps.
>
> **Proof.** Suppose `mᵢ` and `mⱼ` overlap, with `i < j`. Overlapping means
> `mⱼ.start < mᵢ.end`. Because `i < j` we have `i+1 ≤ j`, and sorting gives
> `mᵢ₊₁.start ≤ mⱼ.start`. Chaining these,
>
> ```
> mᵢ₊₁.start ≤ mⱼ.start < mᵢ.end
> ```
>
> so `mᵢ₊₁.start < mᵢ.end`. And `mᵢ.start ≤ mᵢ₊₁.start < mᵢ₊₁.end`. Those are
> exactly the two conditions for `mᵢ` and `mᵢ₊₁` to overlap. ∎

So a conflict anywhere guarantees a conflict between neighbours, and scanning
neighbours is enough. Sorting also simplifies the test itself: since
`previous.start ≤ current.start` is guaranteed, the two-sided overlap check
collapses to the single comparison `current.start < previous.end`.

There is a test for this directly, `sorting still finds a conflict when the
overlapping pair is not adjacent`, which builds a schedule whose overlapping
pair is separated after sorting and confirms a conflict is still reported.

**Running time.** The sort is Θ(n log n) and the scan is Θ(n), so the total is
Θ(n log n), dominated by the sort. Unlike the pairwise version this is Θ(n log n)
in *every* case, including the best one: the sort happens before anything can be
returned early. Extra space is O(n), because `sortedBy` returns a new list rather
than sorting in place.

## Expected growth

| | Best case | Worst case | Extra space |
| --- | --- | --- | --- |
| Pairwise | O(1) | Θ(n²) | O(1) |
| Sort first | Θ(n log n) | Θ(n log n) | O(n) |

Doubling n should roughly quadruple the pairwise time, and slightly more than
double the sorting time (`2n log 2n = 2n log n + 2n`).

## Measured growth

`./gradlew :assignment-1:benchmark` times both on conflict-free schedules, which is
deliberately the worst case, since any conflict lets the pairwise version stop
early and would measure luck rather than scaling. Measured on an M-series Mac,
JDK 21, best of 7 runs after warm-up:

```
      n |   pairwise |  ratio |    sorting |  ratio
--------+------------+--------+------------+-------
   1000 |     0.90 ms |      - |     0.17 ms |      -
   2000 |     4.22 ms |   4.7x |     0.24 ms |   1.5x
   4000 |    11.14 ms |   2.6x |     0.42 ms |   1.7x
   8000 |    55.08 ms |   4.9x |     0.86 ms |   2.1x
  16000 |   240.18 ms |   4.4x |     1.63 ms |   1.9x
```

The adjacent ratios are noisy. The 2.6x at n=4000 is measurement artefact, not
a change in behaviour, since this is a plain timing loop and not a proper JMH
benchmark. The end-to-end figure is far more trustworthy: from n=1000 to
n=16000, a **16× increase in input**, the pairwise time grew **267×** against
the **256×** that n² predicts. The sorting version grew about 10× over the same
range, in the region of the ~22× that n log n predicts and dragged below it by
fixed overheads that matter more at small n.

At n=16000 the sorting version is roughly **150× faster**, and the gap widens
with every doubling.

## Which one would I actually use?

The sorting version, in nearly all cases, but the pairwise version is not
strictly worse. It allocates nothing, it can return after a single comparison
when a conflict is early, and for a handful of meetings the sort's constant
factor dominates. For a personal calendar with a dozen entries the difference is
unmeasurable. The asymptotics only start to matter once n reaches the hundreds,
which the table above shows plainly.
