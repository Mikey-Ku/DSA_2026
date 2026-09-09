# Meeting Scheduler

## What it does

The scheduler checks a list of meetings and reports whether any two of them
overlap. Each meeting has a title, a start time, and an end time.

The program stores times as minutes since midnight. This makes it easier to
compare them. A meeting that ends exactly when another one begins is allowed, so
10:00-11:00 and 11:00-11:30 are not a conflict.

## Checking every pair

The first version compares every meeting with every meeting after it in the list.
It returns when it finds an overlapping pair. If it reaches the end, there is no
conflict.

In the worst case, the number of comparisons grows like n squared. If the number
of meetings doubles, this version can take about four times as much work. It uses
constant extra space because it does not make another list.

## Sorting first

The second version uses Kotlin's `sortedBy` function to put the meetings in start
time order. It then checks each meeting against the meeting directly before it.

Checking neighbors is enough because if a later meeting overlaps an earlier one,
there will also be an overlap between two neighboring meetings in the sorted
list.

Sorting takes Theta(n log n) time, and checking the sorted list takes linear time.
The full algorithm is therefore Theta(n log n). It uses linear extra space
because `sortedBy` creates a new list.

## Tests

The tests run both versions on the same examples. They check schedules with a
conflict, schedules without a conflict, back-to-back meetings, meetings with the
same start time, empty schedules, and larger random schedules. The random tests
also check that the two versions always agree.
