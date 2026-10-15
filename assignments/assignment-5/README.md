# Assignment 5: Divide and Conquer and Dynamic Programming

Michael Ku

Data Structures and Algorithms, Fall 2026

## Part 1: Matrix Class

`Matrix` in `matrix.py` stores an n x n matrix as a list of rows. It supports

- making an n x n matrix of zeros, or one from a square list of rows
- getting and setting the value at a row and column
- splitting into four n/2 x n/2 quarters (A11, A12, A21, A22), which Strassen
  needs
- `A + B`, `A - B` and `A * B` through operator overloading

## Part 2: Strassen's Algorithm

`Matrix` has two ways to multiply. Both return `None` if the matrices are
different sizes.

- `multiply` - the conventional Θ(n³) multiply. Each entry C[i][j] is row i of
  A times column j of B.
- `strassen_multiply` - Strassen's algorithm.

Strassen splits both matrices into quarters and makes 7 half size products
instead of 8

```
M1 = (A11 + A22)(B11 + B22)      C11 = M1 + M4 - M5 + M7
M2 = (A21 + A22) B11             C12 = M3 + M5
M3 = A11 (B12 - B22)             C21 = M2 + M4
M4 = A22 (B21 - B11)             C22 = M1 - M2 + M3 + M6
M5 = (A11 + A12) B22
M6 = (A21 - A11)(B11 + B12)
M7 = (A12 - A22)(B21 + B22)
```

### Testing

Tests are in `tests/test_matrix.py`. They check each matrix operation and a
2 x 2 multiply worked out by hand. Then they check that Strassen gives the same
answer as the conventional multiply on random matrices of many sizes,
including odd sizes that need padding, and at every threshold.

### Benchmarks

`benchmark.py` times each multiply on random n x n matrices with values from
-10 to 10. Each time is the best of 3 runs, measured with `time.perf_counter()`.

| n | Conventional | Pure Strassen | Hybrid (threshold 64) |
|---|---|---|---|
| 16 | 0.0001 | 0.0034 | 0.0001 |
| 32 | 0.0010 | 0.0198 | 0.0008 |
| 64 | 0.0065 | 0.1417 | 0.0064 |
| 128 | 0.0517 | 0.9777 | 0.0476 |
| 256 | 0.4398 | 6.7457 | 0.3384 |

Times are in seconds. Pure Strassen is 15 to 35 times slower than the
conventional multiply at every size. Going all the way down to 1 x 1 makes
millions of tiny lists and does 18 additions per level, which costs far more
than the one multiplication it saves.

### Hybrid threshold

Times at n = 256:

| Threshold | Time (s) |
|---|---|
| 2 | 1.9257 |
| 4 | 0.7937 |
| 8 | 0.4659 |
| 16 | 0.3618 |
| 32 | 0.3300 |
| 64 | 0.3346 |
| 128 | 0.3730 |
| 256 | 0.4382 (plain conventional) |

- **Best threshold:** about 32 to 64.
- **Smaller than that:** the pieces are too small for Strassen to pay off.
- **Bigger than that:** it skips levels where Strassen would have helped.
- **Result:** at n = 256 the hybrid is about 23% faster than the conventional
  multiply, and the gap should grow for bigger n.

## Part 3: Sequence Alignment

`needleman_wunsch.py` uses Needleman-Wunsch for global alignment

- **Grid:** `grid[i][j]` is the best score for the first i letters of one
  sequence against the first j letters of the other. The first row and column
  are all gaps. Every other cell is the best of diagonal (match or mismatch),
  up (gap) and left (gap).
- **Backtrace:** starting from the bottom right corner, it steps back to
  whichever cell the score came from, building the alignment with `-` for gaps.
- **Complexity:** Θ(nm) time and space.

### Testing

Tests are in `tests/test_needleman_wunsch.py`. 

### Result on the Salmonella sequences

`genomeSnippet` against `testAgainst` from the provided `Genome.kt`:

```
Score: 114
Matches: 250 of 374 columns

snippet  TGGCGACAACCGTAGCGGAATATTTTCGCGACCAGGGAAAACGGGTCGTGCTT-TTTATC
         |||| || ||  |||| |||| |||||||||  | ||||| || ||||| |||  ||  |
against  TGGCCACCACGATAGCAGAATTTTTTCGCGATAATGGAAAGCGAGTCGT-CTTGCTTGCC

snippet  GATTCCATGACCCGTTATGCGCGTGCTTTGCGAGACGTGGCACTGGCGTCGGGAGAGCGT
         || ||  |||| ||||||||  | ||    || ||  | || |||||  | ||||||   
against  GACTCACTGACGCGTTATGCCAGGGCCGCACGGGAAATCGCTCTGGCCGCCGGAGAGACC

snippet  CCGGCTCGTCGAGGTTATCCCGCC-TCCGTATTCGATAATTTGCCCCG-CTTGCTGGAAC
          ||| |  | |||  ||| |||||   ||||||   |   ||||| || |||  | ||||
against  GCGGTTTCTGGAGAATAT-CCGCCAGGCGTATTTAGTGCATTGCCACGACTT-TTAGAAC

snippet  GCCCAGGGGCGACCAG-CGAGGGAAGCATTACTGCCTTTTATACGGTACTGCTGGAAAGC
         |  | |||      ||   | || || ||||| || ||||||||||||||| ||||| ||
against  GTAC-GGGAATGGGAGAAAAAGGCAGTATTACCGCATTTTATACGGTACTGGTGGAAGGC

snippet  GAGGAAGAGGCGGACCCGATGGCGGATGAAATTCGCTCTATCCTTGACGGTCA-CCTGTA
         || ||   |   || ||| ||||||||||| | || ||  | ||||| || ||   ||||
against  GATGATATGAATGAGCCGTTGGCGGATGAAGTCCGTTCACTGCTTGATGGACATATTGTA

snippet  TCTGAGCAGAAAGCTGGCCGGGCAGGGACATTACCCGGCAATCGATGTACT-GAAAAGCG
          ||   | ||  ||| || | |  ||| ||||| || || || || ||  | | || || 
against  -CTATCCCGACGGCTTGCAGAGAGGGGGCATTATCCTGCCATTGACGTGTTGGCAACGC-

snippet  TAAGCCGCGTTTTT
         | ||||||||||||
against  TCAGCCGCGTTTTT
```

- **Close match:** 250 of the 374 columns match, about 67%, with only 12 single
  letter gaps.
- **Long exact runs:** `TTTTATACGGTACT` near the middle and `AGCCGCGTTTTT` at
  the end line up exactly.
- **Takeaway:** this fits the BLAST result that the two segments code for
  related proteins.
