# Assignment 4: Sorting Algorithms

Michael Ku

Data Structures and Algorithms, Fall 2026

## Part 1: Sorting Algorithms

Each sort is in its own file in `sorting_algorithms/`. Every one takes a list of
ints and sorts it in place

- `insertion_sort.py` - goes left to right,
  sliding each element left until the one before it is no bigger, so everything
  to its left is always sorted.
- `selection_sort.py` - finds the smallest
  element in the unsorted part and swaps it to the front of that part.
- `merge_sort.py` - splits the list in half,
  sorts each half, then merges the two sorted halves back together.
- `quick_sort.py` - uses the first element as
  the pivot, moves everything smaller to its left and everything bigger to its
  right, then sorts each side.

### Complexity

| Algorithm | Best | Average | Worst |
|---|---|---|---|
| Insertion sort | Θ(n) | Θ(n²) | Θ(n²) |
| Selection sort | Θ(n²) | Θ(n²) | Θ(n²) |
| Merge sort | Θ(n log n) | Θ(n log n) | Θ(n log n) |
| Quick sort | Θ(n log n) | Θ(n log n) | Θ(n²) |

- **Insertion sort:** a backwards list moves every element all the way left,
  1 + 2 + … + (n − 1) = n(n − 1)/2 steps, so Θ(n²). A random list moves each
  element about halfway, still Θ(n²). A sorted list moves nothing, so Θ(n).
- **Selection sort:** every pass scans the whole unsorted part, n(n − 1)/2
  comparisons no matter the input, so every case is Θ(n²).
- **Merge sort:** T(n) = 2T(n/2) + Θ(n), which the master theorem gives as
  Θ(n log n) in every case.
- **Quick sort:** partitioning is Θ(n). Even splits give T(n) = 2T(n/2) + Θ(n)
  = Θ(n log n). If the pivot is always the smallest or largest element,
  T(n) = T(n − 1) + Θ(n) = Θ(n²). 

## Part 2: Testing

Tests are in `tests/test_sorting.py`. They run every sort on the same lists and
compare each result with Python's `sorted()`

## Part 3: Benchmarking

`benchmark.py` times every sort on random lists of 10, 100, 1,000, 10,000, and
100,000 ints and prints the average time for each one.
- **Input:** random ints from 0 to 999
- **Trials:** each size is run 5 times, with a new random list each time, and
  the table shows the average. 
- **Sync:** in each trial every sort gets its own copy of the same list.
- **Timing:** `time.perf_counter()`

### Results

Average time in seconds over 5 runs:

| n | Insertion sort | Selection sort | Merge sort | Quick sort |
|---:|---:|---:|---:|---:|
| 10 | 0.000002 | 0.000002 | 0.000004 | 0.000002 |
| 100 | 0.000047 | 0.000053 | 0.000041 | 0.000021 |
| 1,000 | 0.005598 | 0.006623 | 0.000558 | 0.000326 |
| 10,000 | 0.628435 | 0.726112 | 0.007741 | 0.004833 |
| 100,000 | 65.119333 | 67.199116 | 0.094040 | 0.107925 |

### Conclusions

- **Small lists don't matter much.** At 10 items every sort takes a few
  microseconds. Merge sort is slowest there because making the new lists costs more
  than the sorting.
- **Insertion and selection sort grow with n².** Each 10× increase in n makes
  them about 100× slower 
- **Merge and quick sort grow like n log n.** Each 10× increase makes them about
  12 to 22× slower
- **Larger Values = larger differences.** At 100,000 items the n log n sorts are about 600 to 700
  times faster
- **Quick sort vs merge sort.** Quick sort was fastest up to 10,000 since it
  sorts in place. At 100,000 merge sort edged ahead, because with values from 0
  to 999 there are lots of repeats, which gives pivots lopsided
  splits.
- **General take:** for anything beyond a few hundred items, use an n log n sort and
  Insertion sort is only reasonable for very small lists.

## Extra Credit: Zig-zag Sort

My writeup on Goodrich's Zig-zag Sort is in [`ZigZagSort.pdf`](ZigZagSort.pdf).
