# Assignment 1: Hello World and Getting to Know You

Michael Ku

Data Structures and Algorithms, Fall 2026

## Part 1: Course Entry Survey

I submitted the course entry survey through the Google Form.

## Part 2: Learning Strategies

### 1. When has learning gone well for you, and what strategies helped?

A good example for me was teaching myself machine learning. I watched YouTube
videos, looked at other people's work, talked through ideas, and used AI as a
tutor. The biggest thing was actually building things and learning through trial
and error. Making mistakes and then fixing them helped the ideas stick.

### 2. What strategies have made learning less effective or less enjoyable?

Back-to-back lectures without enough time to practice do not work well for me. In
a class last semester, I sometimes got lost during one topic and then had trouble
with the next topic because everything built on what came before it. There were
also not many CAs available to help.

I learn better when I have examples and practice problems at each step. They give
me something specific to work on and make it easier to ask useful questions.

### 3. How are you thinking about AI tools in this course?

I agree that copying answers from AI does not help someone learn. The useful part
of a problem is struggling with it enough to understand what is happening.

I mainly see AI as a tutor. I can show it my reasoning, ask for feedback, and ask
follow-up questions when I am stuck. My goal is to use it for explanations or
hints, not as a replacement for doing the work myself.

### 4. What strategies will you use to be successful?

My main strategy will be practice. Data structures and algorithms are taught in
many places, so there are a lot of practice problems and other resources I can
use.

I want to try each problem myself first. If I get stuck, I can ask for a hint or
an explanation and then keep working instead of asking for the full answer.

### 5. What do you think about the proposed oral quiz activities?

I like the idea of oral quizzes because they let me explain what I know instead
of only giving a final answer. They also feel similar to code reviews and
technical interviews.

I am less sure about reading code I did not write because people can write the
same idea in very different ways. I am still open to trying it, especially if the
code uses patterns we have already seen in class.

### 6. How can the teaching team support you?

It would help to have people available when I have questions, especially if I
start falling behind. Practice material and examples would also help me check my
understanding. Other than that, I hope the class stays fun and interesting.

## Part 3: Hello World

I finished the beginner Kotlin tour and attempted the exercises.

### 1. What features do you like about Kotlin?

I like that Kotlin feels familiar after using Java. Functions, classes, and basic
data structures work in ways that mostly make sense to me. I also like static
typing because I got used to it while working with TypeScript. It helps catch
mistakes before the program runs. Kotlin can also figure out many types on its
own, so the code does not need as much repeated information as Java.

### 2. Were you expecting anything that you did not find?

There was not anything major missing that I expected to find. Most of the basic
features felt familiar because of my Java experience. I was surprised by how
short some Kotlin code can be, especially when it figures out types automatically.

### 3. What questions do you have?

I want to learn more about how Kotlin performs compared with Java and other
languages. I also want to understand how Kotlin libraries are added to a project
and how Gradle manages them.

### 4. Were you able to use the debugger?

I have used interactive debuggers before. I was able to launch the Kotlin
debugger and try its basic features.

## Part 4: Translating Old Code

I translated three Python programs from a previous Software Design assignment:

1. A Markov text generator that creates sentences based on which words followed
   each other in the original text.
2. An instant-runoff voting program that counts ranked ballots and removes the
   lowest candidate each round.
3. A Koch snowflake program that repeatedly replaces line segments to build the
   snowflake shape.

The Kotlin files are in `src/main/kotlin/translation`. The tests are in
`src/test/kotlin/translation`, and the original Python files are in
`reference/python`.

My response about the translation process is in `docs/translation-writeup.md`.

## Part 5: Meeting Scheduler

The meeting scheduler checks whether any two meetings overlap. The two required
versions are in `src/main/kotlin/scheduler/Scheduler.kt`.

- `conflictByPairs` checks every possible pair. Its worst-case running time
  is Theta(n squared).
- `conflictBySort` sorts the meetings and then checks neighboring
  meetings. Its running time is Theta(n log n).

The scheduler tests include overlapping meetings, back-to-back meetings, empty
schedules, and schedules in different orders. More information is in
`docs/meeting-scheduler.md`.

To run both algorithms on the two example schedules from day 1, run this from
the repository root:

```bash
./gradlew :assignment-1:run
```
