plugins {
    // Lets Gradle locate, and if necessary download, the JDK the build asks for,
    // so `./gradlew` works on a machine whose default `java` is too old or absent.
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

rootProject.name = "DSA_2026"

// One subproject per assignment. Add new assignments here as they arrive.
include("assignment-1")
