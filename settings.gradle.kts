plugins {
    // Lets Gradle locate, and if necessary download, the JDK the build asks for,
    // so `./gradlew` works on a machine whose default `java` is too old or absent.
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

rootProject.name = "DSA_2026"

// One subproject per Kotlin assignment. Add new ones here as they arrive.
// Assignment 2 is written in Python, so it is not part of the Gradle build.
include("assignment-1")
project(":assignment-1").projectDir = file("assignments/assignment-1")
