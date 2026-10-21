# PageRank: ranking web pages and NFL teams

Michael Ku

Data Structures and Algorithms, Fall 2026

This project has three parts:

1. **The algorithm:** PageRank, run on a real web graph.
2. **The math:** why PageRank is an eigenvector of the Google matrix.
3. **An application:** ranking the 2025 NFL teams and predicting the playoffs.

## What PageRank is

PageRank scores pages using only the links between them. A link from page A
to page B is a vote for B. Votes from high-scoring pages count for more than
votes from low-scoring pages.

Because every score depends on other scores, PageRank computes them step by
step. Let N be the number of pages and d = 0.85 the damping factor.

1. Every page starts with score 1/N. The scores always add up to 1.
2. Each page splits d of its score evenly among the pages it links to.
3. The other 1 − d of every score is spread evenly over all pages, so no page
   drops to zero.
4. A page with no outgoing links (a dead end) spreads its whole score evenly
   over all pages.
5. Repeat until the scores stop changing. The final scores are the PageRank.

The idea behind it is a random surfer. On each page they click a random link
with probability d, or jump to a random page with probability 1 − d. A page's
PageRank is the fraction of time the surfer spends there.

## Part 1: The algorithm

**Data:** the web-Stanford graph from SNAP, a 2002 crawl of stanford.edu with
281,903 pages and 2,312,497 links. Pages are numbered, not named.

`pagerank.py` has three functions:

- `load_graph` reads the file, where each line is one link `from to`. It
  stores the graph as a dictionary mapping each page to the set of pages it
  links to.
- `pagerank` runs the steps above. Each pass gives every page the random-jump
  and dead-end share, then adds each page's link share to the pages it links
  to. It stops when the total change in scores is below 10⁻⁶.
- `top_pages` returns the highest-scoring pages.

**Running time:** each pass visits every page and every link once, so it is
O(N + E), where E is the number of links. One pass takes about 0.16 seconds,
and d = 0.85 needs 63 passes, about 10 seconds in total.

Top 10 pages with d = 0.85:

| # | Page | PageRank |
|---|---|---|
| 1 | 89073 | 0.011303 |
| 2 | 226411 | 0.009268 |
| 3 | 241454 | 0.008297 |
| 4 | 262860 | 0.003023 |
| 5 | 134832 | 0.003001 |
| 6 | 234704 | 0.002572 |
| 7 | 136821 | 0.002454 |
| 8 | 68889 | 0.002431 |
| 9 | 105607 | 0.002391 |
| 10 | 69358 | 0.002364 |

## Part 2: PageRank as an eigenvector

### Eigenvectors

An **eigenvector** of a matrix G is a vector v that G only scales:

    G v = λ v

The number λ is its **eigenvalue**. When λ = 1, multiplying by G leaves v
exactly the same.

That is what happens at the end of PageRank. Each new score is a weighted sum
of the old scores, so one pass is a matrix multiplication. When the scores
stop changing, they are a vector the matrix leaves the same. So **PageRank is
the eigenvector of that matrix with eigenvalue 1.**

### The Google matrix

The **Google matrix** G is the matrix that performs one pass of PageRank. It
has one row and one column per page. Entry G[i][j] is the probability that
the random surfer moves from page j to page i. Each column adds up to 1.

G is built from two parts:

- **Link matrix S:** column j puts 1/k on each of the k pages that page j
  links to. If page j is a dead end, its column puts 1/N on every page.
- **Random jumps:** (1 − d)/N added to every entry.

Together:

    G = d·S + (1 − d)/N

One pass of PageRank is `r_new = G · r`, where r is the list of scores. The
final scores don't change on another pass, so `r = G · r`. That is the
eigenvector equation with λ = 1.

### Two ways to get the same scores

**Way 1: the loop** (`pagerank()` in `pagerank.py`). Start with equal scores
and do passes until they stop changing. This is what Part 1 does. Its
textbook name is *power iteration*, because it keeps multiplying by G.

**Way 2: numpy** (`eigen_check.py`). Write out the whole matrix G and call
`numpy.linalg.eig`, which solves for the eigenvectors directly. Take the one
with eigenvalue 1 and scale it to add up to 1. No passes are involved.

If PageRank really is the eigenvector of G, both ways should give the same
scores. To test this, `eigen_check.py` runs both on a 1,000-page piece of
web-Stanford (the pages reached by following links out from the top page,
89073). The full graph is too big for numpy, because G would have 281,903²
entries.

**Result:** the two ways agree. On every page, the scores differ by at most
0.000000000001 (10⁻¹²). That tiny gap is expected: for this check the loop
stops once the scores change by less than 10⁻¹², so it is only that close to
the exact answer. numpy also finds that the largest eigenvalue is 1.0000.

So the loop in Part 1 really is finding the eigenvector of the Google matrix.
The eigenvector explains *what* PageRank is, and the loop is a simple way to
compute it.

## Part 3: Ranking NFL teams

PageRank works on any graph, not only web pages. For a football season:

- Each **team** is a node.
- Each **loss** adds a link from the loser to the winner, so a loss is a vote
  for the team that beat you.

This means beating a strong team is worth more than beating a weak one, which
win percentage does not account for.

**Data:** the 2025 season from nflverse's `games.csv`: 272 regular-season
games and 13 playoff games. Losing to the same team twice gives one link, and
the season's one tie is left out.

### Regular-season rankings

| # | Team | PageRank | Record | Win % |
|---|---|---|---|---|
| 1 | LA | 0.0693 | 12-5 | 0.706 |
| 2 | SEA | 0.0666 | 14-3 | 0.824 |
| 3 | SF | 0.0569 | 12-5 | 0.706 |
| 4 | TB | 0.0515 | 8-9 | 0.471 |
| 5 | JAX | 0.0508 | 13-4 | 0.765 |
| 6 | HOU | 0.0473 | 12-5 | 0.706 |
| 7 | PHI | 0.0447 | 11-6 | 0.647 |
| 8 | BUF | 0.0391 | 12-5 | 0.706 |
| 9 | DEN | 0.0383 | 14-3 | 0.824 |
| 10 | LAC | 0.0360 | 11-6 | 0.647 |

- Seattle, the Super Bowl winner, ranks 2nd.
- Tampa Bay ranks 4th with an 8-9 record, ahead of 15 teams with a better
  win percentage.
- New England went 14-3 and reached the Super Bowl, but ranks 11th.

### Predicting the playoffs

To measure accuracy, `nfl_rankings.py` predicts each playoff game and checks
the prediction against the real result. The team with the higher PageRank is
the pick.

1. Rank the teams using the regular season.
2. Pick every game in the next playoff round.
3. Add that round's real results to the graph and rerun PageRank.
4. Repeat through the Super Bowl.

As a baseline, the same games are also picked by higher win percentage,
updated the same way.

| Round | Games | PageRank correct | Win % correct |
|---|---|---|---|
| Wild Card | 6 | 4 | 5 |
| Divisional | 4 | 2 | 4 |
| Conference | 2 | 1 | 2 |
| Super Bowl | 1 | 1 | 0 |
| **Total** | **13** | **8 (62%)** | **11 (85%)** |

PageRank was correct on 8 of 13 games (62%). Win percentage was correct on
11 (85%). Updating the rankings after each round helped PageRank by one game:
without the updates it got 7. With only 13 games, these results are a small
sample.

### Why PageRank did worse

In this graph, a team's score comes only from the teams it beat. A loss
never lowers the losing team's score, it only decides where that team's
vote goes. Two examples:

- Tampa Bay ranks 4th because it beat Seattle (#2), San Francisco (#3) and
  Houston (#6). Its nine losses cost it nothing.
- New England ranks 11th because 8 of the 12 teams it beat rank 17th or
  lower. PageRank picked against them in their first two playoff games, and
  they won both.

Every win also counts the same, whether by 1 point or 30.

## Conclusion

- **Algorithm:** PageRank passes score along links until the scores settle.
  With the graph stored as a dictionary of outgoing links, each pass is
  O(N + E), and the full 281,903-page graph runs in about 10 seconds.
- **Math:** one pass is multiplication by the Google matrix, so PageRank is
  its eigenvector with eigenvalue 1. numpy's eigenvector matched `pagerank()`
  to within 10⁻¹², so the loop really is finding that eigenvector.
- **NFL:** PageRank rewards strength of schedule but ignores losses. On the
  2025 playoffs it picked 8 of 13 games correctly, compared with 11 for win
  percentage. Possible improvements are weighting links by point margin or
  combining PageRank with win percentage.

