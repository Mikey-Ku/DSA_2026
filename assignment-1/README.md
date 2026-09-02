# Assignment 1: Hello World and Getting to Know You

Michael Ku
Data Structures and Algorithms, Fall 2026

## Part 1: Course Entry Survey

Submitted through the Google Form. Nothing in this repo.

## Part 2: Identifying Effective Strategies for Learning

### 1. Choose a moment in your educational career where learning went really well. What strategies did you use that worked particularly well?

**Answer:**

A moment that worked really well for me was teaching myself machine learning. A
few things helped. I watched as many YouTube videos as I could, but most of the
learning came from doing: building things, looking at other people's work, having
conversations about it, and using AI as a tutor. The biggest factor was trial and
error. I kept testing things, kept trying, and kept challenging myself. Making
mistakes is what made things stick. The more mistakes I made, the more I
remembered and the better I understood.


### 2. Which strategies have led to less effective learning, or less enjoyment of the learning experience?

**Answer:**

Back-to-back lectures without enough practice in between. In a class I took last
semester, I would sometimes get lost partway through a topic and not be able to
get the help I needed. The material was fairly experimental and there were not
many CAs available. Because each lesson built on the one before it, falling
behind on one thing made the next one harder, and it was difficult to catch up.

What I want to avoid this time is being in that position without examples to work
from. If there are practice examples at every step, I have something concrete to
ask about. Without them it is hard to ask a question that is actually relevant,
or to know what direction to go in.


### 3. The instructor's view is that grappling with a problem is what makes the concepts stick, and that prompting an AI for answers and copying them does not get you there. Do you agree with this framing? How are you thinking about AI tools in this course?

**Answer:**

I agree with the framing. Having AI produce your answers for you does hurt your
learning.

That said, I have always thought of AI as one of the best tutors available. I use
it as a tutor because I can ask questions continuously, give it my own reasoning
and get feedback on it, and keep asking follow-ups without feeling like I am
wasting someone's time.

I think it comes down to how you use it and how you view it. This course covers
material that is taught everywhere and is well documented online, and it is not
extremely technically complicated, so AI is going to be useful here. The
important part is the balance, and not reaching for it to answer every question.


### 4. What strategies will you use in this course to be successful? With respect to AI, what principles will you use?

**Answer:**

Mainly practice. This class is foundational to a lot of computer science, so
there are a large number of resources and contest problems available. I plan to
use those and work through as many problems as I can.

For AI, my principle is to challenge myself first. If I get properly stuck, I
will ask for a hint or a way to move forward rather than for the answer, so that
I can keep going and get more practice. The more problems I see, the better I
will get and the more I will understand.


### 5. What do you think of the proposed activities for the oral quizzes? Would you add or subtract any?

**Answer:**

I like oral quizzes. I think they are one of the best ways to actually
demonstrate what you know, and they are close to what the industry does with code
review and technical interviews, where you sit down, look at code, and talk
through it.

The one activity I am less sure about is reading code I did not write, unless it
is fairly standard, because there can be a lot of variability in how people write
things. For this class I am not too worried, since a lot of the material is
fairly cut and dry.


### 6. How can the teaching team support you?

**Answer:**

Being available when I have questions, and being willing to help when I feel
behind. Beyond that, providing plenty of material to work through, and keeping
the class fun. I think this is going to be an enjoyable class.


---

## Part 3: Hello World

I read the *Getting Set with Kotlin* page and worked through the beginner Kotlin
tour, attempting the exercises.

### 1. What features do you like about Kotlin?

**Answer:**

One of the main things I like about Kotlin is how familiar it feels coming from
Java. Many of its basic concepts, such as functions, classes, and common data
structures, translate fairly easily from what I already know. I also like that
Kotlin is statically typed. After becoming comfortable with TypeScript, I have
come to appreciate having types checked before running a program because it makes
the code clearer and helps catch mistakes. At the same time, Kotlin's type
inference means that I do not always have to explicitly write each type, which
keeps the code concise.


### 2. Are there things you were expecting to find that you haven't?

**Answer:**

There was not anything major that I expected to find but did not. Since Kotlin
shares many concepts with Java, most of its basic features felt familiar.
However, I was surprised by how concise Kotlin's syntax can be compared with
Java, especially because of features such as type inference and its simpler
function syntax.


### 3. What questions do you have?

**Answer:**

I do not have any immediate questions because I usually learn a new language by
experimenting with it and seeing how its different features behave. However, I am
curious about how Kotlin's efficiency and performance compare with Java and other
languages. I would also like to learn more about the libraries available for
Kotlin and how external libraries are added to and used within a project.


### 4. Did you use the debugger? Do you have experience with interactive debuggers? Were you able to launch it?

**Answer:**

I have experience using interactive debuggers like this one. I was able to
successfully launch the Kotlin debugger and experiment with its basic
functionality.


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


## Part 5: Implementing Meeting Scheduler

Determines whether a collection of meetings contains a conflict. Meetings are
half-open intervals `[start, end)`, so a meeting ending exactly when another
begins is not a conflict.

Both required algorithms are in `src/main/kotlin/scheduler/Scheduler.kt`:

- `findConflictByPairs`: the straightforward version, comparing every pair
- `findConflictBySorting`: sorts by start time with Kotlin's built-in
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
