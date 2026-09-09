plugins {
    kotlin("jvm") version "2.4.10"
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

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("passed", "failed", "skipped")
    }
}
