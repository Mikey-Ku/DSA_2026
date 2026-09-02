# DSA 2026

Coursework for Data Structures and Algorithms, 2026.

| Assignment | Topic | Notes |
| --- | --- | --- |
| [assignment-1](assignment-1) | Hello world, translating old code, meeting scheduler | Kotlin port of three Python programs + conflict detection, 83 tests |

## Building

This is a Gradle multi-project build with one subproject per assignment. The
Gradle wrapper is checked in, so no local Gradle install is needed, and the
build declares the JDK it wants. Gradle locates or downloads a JDK 21 itself
rather than relying on whatever `java` happens to be on `PATH`.

Run everything from this directory:

```bash
./gradlew build              # compile and test every assignment
./gradlew test               # run every assignment's tests
./gradlew :assignment-1:run  # run one assignment's demo
```

Each assignment has its own README with details on what it contains.

## Opening in an editor

Open **this** folder (`DSA_2026`), not an individual assignment folder. The
Gradle build lives here, and that is what an IDE needs in order to resolve
imports and offer completion.
