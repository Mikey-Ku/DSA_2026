# Translating My Old Code to Kotlin

## What I translated

I translated three Python programs from an old Software Design assignment. One
generates text using a Markov chain, one runs an instant-runoff election, and one
creates the points for a Koch snowflake. I also translated the tests so I could
check that the Kotlin versions still behaved like the Python versions.

## What went well

Kotlin felt familiar because I have used Java before. Static types helped me see
what each function expected, and the compiler caught some mistakes before I ran
the tests. Data classes were also useful for things like points and election
results because the values had names instead of just being positions in a tuple.

Kotlin's `tailrec` feature worked well for the recursive voting and snowflake
functions. It lets Kotlin run those recursive functions without building up a
large call stack.

I also changed the text generator so a random number generator can be passed into
it. This made the tests repeatable because they can use the same random seed each
time.

## What was difficult

The project setup took more work than Python because Kotlin needed Gradle, a JVM,
and the correct project structure before I could run anything.

Some functions that looked similar between the languages did not behave in the
same way. For example, Python's `split()` handles repeated spaces and newlines,
while the simple Kotlin version did not. I had to use a regular expression so the
same text produced the same list of words.

The geometry code also used a few Java math functions because Kotlin does not
include its own degree conversion functions. The tests needed small helper
functions for comparing decimal values because floating-point results are not
always exactly equal.

## What I learned

The hardest part was understanding code that changed a list while looping over
it. Instead of translating that part line by line, I first worked out what it was
trying to do and then wrote a simpler Kotlin version with the same result.

This assignment showed me that translating code is not only changing the syntax.
I also had to understand the behavior of the original program, learn where the
two languages act differently, and use tests to make sure I did not accidentally
change the result.
