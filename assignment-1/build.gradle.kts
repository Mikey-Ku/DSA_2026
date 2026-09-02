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
 * Time the two meeting-conflict algorithms on schedules of increasing size, to
 * check the predicted growth rates against measured ones.
 */
tasks.register<JavaExec>("benchmark") {
    group = "verification"
    description = "Time the pairwise and sorting conflict detectors as n grows."
    mainClass.set("scheduler.BenchmarkKt")
    classpath = sourceSets["main"].runtimeClasspath
}
