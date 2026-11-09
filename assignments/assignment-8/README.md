# Assignment 8: K-D Trees and Nearest Neighbor Search

Michael Ku

Data Structures and Algorithms, Fall 2026

## Part 1: K-D Tree and Brute Force

### K-D Tree

`KDTree` in `kd_tree.py` stores points with any number of dimensions (k) and
finds the point closest to a query point, using Euclidean distance.

- `KDTree(points)` builds a balanced tree from a list of k-dimensional points.
- `nearest(query)` returns the point in the tree that is closest to `query`.

**Building the tree**

1. Find the median of the points along dimension 0.
2. Put points below the median in the left group and points at or above it in
   the right group.
3. Build each group the same way, using the next dimension. After dimension
   k - 1, go back to dimension 0.
4. Stop when a group has one point left. That point becomes a leaf.

There are two kinds of nodes. A `Split` node stores the dimension it splits on
and the median value. A `Leaf` node stores one point, so every point ends up in
a leaf. Because every split is at the median, both sides get about half the
points, and the tree is about log₂ n levels deep.

**Handling ties**

- If no point in the group is below the median (for example, many points share
  the smallest value), the split uses the next bigger value instead, so the left
  side is never empty.
- If every point in the group has the same value on a dimension, that dimension
  can't split them, so it moves on to the next dimension.
- If all the points in a group are identical, they become a single leaf.

**Searching**

1. Walk down the tree like a binary search tree: go left if the query's value is
   below the median, otherwise go right.
2. At the leaf, save that point as the best so far, along with its distance to
   the query.
3. On the way back up, check the other branch at each split only if the
   splitting line is closer to the query than the best point so far. If it
   isn't, nothing on the other side can be closer, so the whole branch is
   skipped.


### Quickselect

The median at each level is found with quickselect instead of sorting:

1. Pick a random pivot and partition the points around it, with smaller values
   on the left and bigger values on the right.
2. If the pivot lands in the median's position, stop.
3. Otherwise, repeat on just the side that contains the median.

Each round throws away part of the list, so quickselect takes Θ(n) time on
average, compared to Θ(n log n) for sorting. Choosing the pivot at random means
already-sorted input doesn't cause the Θ(n²) worst case.

After quickselect, the list is already split around the median. One more pass
moves every point below the median to the front, so the left and right groups
are just the two halves of the list. With Θ(n) work per level and about log₂ n
levels, building the whole tree takes Θ(n log n).

### Brute Force

`brute_force_nearest` in `brute_force.py` computes the distance from the query
to every point and returns the closest one. Each query takes Θ(nk).

### Testing

The tests are in `tests/test_kd_tree.py`. They check:

- quickselect and the median split
- the tree's structure on a small hand-checked example and on random points
- nearest neighbor results against brute force, including when there are
  duplicate points

## Part 2: Benchmarking

`run_experiment(k, num_points)` in `benchmark.py` creates:

- `num_points` random k-dimensional training points (the points being searched)
- 1000 random query points (the points to find neighbors for)

Every coordinate is a random number between 0 and 1. The function returns three
times in seconds, measured with `time.perf_counter()`:

1. the time to build the tree
2. the time to answer all 1000 queries with the tree
3. the time to answer all 1000 queries with brute force

It also checks that the tree and brute force found the same neighbor for every
query.

`main()` runs every combination of k = 1, 2, 3, 5, 10, 20 and
num_points = 10, 100, 1,000, 10,000, 100,000.

## Part 3: Results

### Times

All times are in seconds. Query times are for all 1000 queries together.

| k | Points | Build tree | Tree queries | Brute force |
|---|---:|---:|---:|---:|
| 1 | 10 | 0.0000 | 0.0008 | 0.0019 |
| 1 | 100 | 0.0002 | 0.0011 | 0.0150 |
| 1 | 1,000 | 0.0021 | 0.0012 | 0.1253 |
| 1 | 10,000 | 0.0241 | 0.0015 | 1.0706 |
| 1 | 100,000 | 0.2796 | 0.0022 | 10.7971 |
| 2 | 10 | 0.0000 | 0.0012 | 0.0015 |
| 2 | 100 | 0.0001 | 0.0016 | 0.0127 |
| 2 | 1,000 | 0.0018 | 0.0020 | 0.1284 |
| 2 | 10,000 | 0.0237 | 0.0025 | 1.2937 |
| 2 | 100,000 | 0.2984 | 0.0032 | 13.0951 |
| 3 | 10 | 0.0000 | 0.0016 | 0.0017 |
| 3 | 100 | 0.0001 | 0.0030 | 0.0154 |
| 3 | 1,000 | 0.0018 | 0.0041 | 0.1523 |
| 3 | 10,000 | 0.0234 | 0.0050 | 1.5545 |
| 3 | 100,000 | 0.2959 | 0.0075 | 15.5254 |
| 5 | 10 | 0.0000 | 0.0025 | 0.0022 |
| 5 | 100 | 0.0001 | 0.0089 | 0.0193 |
| 5 | 1,000 | 0.0018 | 0.0163 | 0.1938 |
| 5 | 10,000 | 0.0241 | 0.0252 | 1.9635 |
| 5 | 100,000 | 0.3201 | 0.0398 | 19.9047 |
| 10 | 10 | 0.0000 | 0.0040 | 0.0032 |
| 10 | 100 | 0.0001 | 0.0364 | 0.0292 |
| 10 | 1,000 | 0.0019 | 0.2752 | 0.2975 |
| 10 | 10,000 | 0.0239 | 0.9714 | 3.0249 |
| 10 | 100,000 | 0.3648 | 2.1410 | 29.9790 |
| 20 | 10 | 0.0000 | 0.0060 | 0.0055 |
| 20 | 100 | 0.0001 | 0.0606 | 0.0494 |
| 20 | 1,000 | 0.0019 | 0.6331 | 0.5002 |
| 20 | 10,000 | 0.0246 | 6.4262 | 5.0821 |
| 20 | 100,000 | 0.3526 | 73.8122 | 50.4283 |

### When K-D Trees Win

- **Many points, few dimensions: the tree wins by a lot.** For k = 1 to 5 with
  10,000 or more points, building the tree and running all 1000 queries takes
  under 0.4 s, while brute force takes 1 to 20 s. Brute force gets about 10
  times slower for every 10 times more points, because it checks every point.
  The tree's query time barely changes. For k = 1, it only goes from 0.0012 s
  at 1,000 points to 0.0022 s at 100,000 points. Each query goes about log₂ n
  levels down and skips most of the tree.
- **Few points: no real difference.** With only 10 points, brute force does
  just 10 distance checks per query. The tree's recursion costs about the same,
  so both finish in a few milliseconds.
- **High dimensions: the tree stops helping.** At k = 10, the tree is about
  even with brute force at 1,000 points and only pulls clearly ahead from
  10,000 points. At k = 20, it is slower than brute force at every size. In
  high dimensions, random points are all about the same distance from each
  other. The splitting line is almost always closer than the best point found
  so far, so the search can't skip either branch. It ends up visiting nearly
  every node and also pays for the recursion. 
  
- **Building the tree pays for itself quickly.** Building takes about 0.3 s for
  100,000 points. One brute force query on 100,000 points takes about 0.01 s,
  so at low k the build time is paid back after about 30 queries. If the same
  points will be searched more than a handful of times, the tree is worth
  building.
