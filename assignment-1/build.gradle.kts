plugins {
    kotlin("jvm") version "2.4.10"
    application
}

group = "edu.olin.dsa2026"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(kotlin("test"))
}

kotlin {
    // Pin the toolchain so the build does not depend on whichever JDK happens
    // to be first on PATH. Gradle downloads a matching JDK if one is missing.
    jvmToolchain(21)
}

application {
    mainClass.set("MainKt")
}

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("passed", "failed", "skipped")
    }
}

/**
 * Print this port's next-word maps for the shared corpus, in the same format as
 * `reference/python/crosscheck.py`. `reference/crosscheck.sh` diffs the two.
 */
tasks.register<JavaExec>("crossCheck") {
    group = "verification"
    description = "Print next-word maps for reference/corpus.txt, for diffing against the Python original."
    mainClass.set("CrossCheckKt")
    classpath = sourceSets["main"].runtimeClasspath
    args(layout.projectDirectory.file("reference/corpus.txt").asFile.path)
}
