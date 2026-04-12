---
name: maven-to-gradle-migrator
description: >
  Migrate Java Maven projects to Gradle — single-module or multi-module. Use this skill
  whenever the user wants to convert pom.xml to build.gradle, switch a Maven repo to Gradle,
  migrate a multi-module Maven project to a multi-module Gradle project, or needs help
  producing a valid Gradle multi-module output structure (settings.gradle, subproject
  build files, version catalog, etc.). Also handles partial migrations, specific plugin
  translations, or converting Maven dependency management to Gradle platforms.
  Trigger on: "migrate to gradle", "convert pom.xml", "switch from maven", "gradle init pom",
  "maven to gradle", "multi-module gradle", "gradle wrapper", "replace pom with build.gradle".
---

# Maven to Gradle Migrator

Structured workflow for migrating Java projects from Maven to Gradle. Supports single-module
and multi-module projects, both as input (Maven source) and as output (Gradle structure). You
choose between Groovy DSL (`build.gradle`) and Kotlin DSL (`build.gradle.kts`) depending on
the project's needs.

## Prerequisites

- `java` must be installed (Java 8+; Gradle 8.x requires Java 8+).
- `gradle` must be available (version 7+ recommended; version 8+ for Kotlin DSL and version
  catalogs). If Gradle is not installed, set up the wrapper first (see Step 2).
- The Maven project must be accessible locally.

---

## Step 1 — Detect Project Structure

Identify whether the project is single-module or multi-module before doing anything else.

```bash
# Check for modules in the root pom
grep -l "<modules>" pom.xml 2>/dev/null && echo "MULTI-MODULE" || echo "SINGLE-MODULE"
```

Then run the analysis script (locate it inside the plugin's `scripts/` directory):

```bash
python <skill-scripts-dir>/analyze_maven.py [path/to/pom.xml]
```

The script recursively walks all sub-modules and reports: project coordinates, modules list,
plugins, profiles, and `<dependencyManagement>` entries per module. Review its output to
understand complexity before migrating.

**What to look for:**
- Number of modules and nesting depth
- Custom or corporate Maven plugins (need manual Gradle equivalents)
- Active Maven profiles (no direct Gradle equivalent — need conditional logic)
- `<dependencyManagement>` blocks (becomes a Gradle platform or version catalog)
- Inherited `<parent>` relationships across modules

---

## Step 2 — Set Up the Gradle Wrapper

Always use the Gradle wrapper (`./gradlew`) for reproducibility. If Gradle is installed:

```bash
cd /path/to/project-root
gradle wrapper --gradle-version 8.7
```

If Gradle is not installed, download the wrapper bootstrap:

```bash
# Download wrapper bootstrap (no Gradle installation required)
curl -sL https://services.gradle.org/distributions/gradle-8.7-bin.zip -o /tmp/gradle.zip
# Or use the official Gradle wrapper installer script:
# https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:adding_wrapper
```

Commit `gradlew`, `gradlew.bat`, and `gradle/wrapper/gradle-wrapper.properties` into version control.

---

## Step 3 — Choose Your DSL

| Groovy DSL (`build.gradle`) | Kotlin DSL (`build.gradle.kts`) |
|-----------------------------|---------------------------------|
| Default output of `gradle init` | Requires `--dsl kotlin` flag |
| Dynamic, concise syntax | Statically typed, IDE-friendly |
| More examples online | Better for large teams, refactoring |
| Any Gradle version | Gradle 5+ (fully stable in 7+) |

**Default:** use Groovy DSL unless the user specifically asks for Kotlin DSL or the project
already uses Kotlin.

---

## Step 4 — Run Automatic Conversion

The `gradle init --type pom` command generates the initial Gradle build files from `pom.xml`.
Run it from the project root.

```bash
# Single-module OR multi-module root:
cd /path/to/project-root
gradle init --type pom --dsl groovy    # Groovy DSL (default)
# OR
gradle init --type pom --dsl kotlin   # Kotlin DSL
```

**What `gradle init` produces for a multi-module project:**
- `settings.gradle` (or `.kts`) — includes all sub-projects
- Root `build.gradle` — common configuration via `allprojects {}` / `subprojects {}`
- Each module gets its own `build.gradle` with its dependencies

**Important:** `gradle init` does a good job for simple cases but almost always needs
refinement for real-world projects (see Steps 5 and 6).

---

## Step 5 — Validate and Fix Multi-Module Structure

### 5a — Verify `settings.gradle`

Every sub-module must be declared in `settings.gradle`:

```groovy
// settings.gradle (Groovy)
rootProject.name = 'my-project'
include 'module-a'
include 'module-b'
include 'module-c'
include 'module-a:sub-module'   // Nested modules use colon separator
```

```kotlin
// settings.gradle.kts (Kotlin DSL)
rootProject.name = "my-project"
include("module-a", "module-b", "module-c")
include("module-a:sub-module")
```

Cross-check the declared modules against the Maven `<modules>` list and the actual directory
structure. A missing `include` means Gradle silently ignores that module.

### 5b — Centralize Shared Configuration

Maven's `<parent>` POM shared config becomes Gradle's `subprojects {}` or `allprojects {}`
block in the root `build.gradle`:

```groovy
// Root build.gradle (Groovy)
subprojects {
    apply plugin: 'java'

    java {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    repositories {
        mavenCentral()
    }

    dependencies {
        testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
    }
}
```

For Kotlin DSL:

```kotlin
// Root build.gradle.kts
subprojects {
    apply(plugin = "java")

    configure<JavaPluginExtension> {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    repositories {
        mavenCentral()
    }

    dependencies {
        "testImplementation"("org.junit.jupiter:junit-jupiter:5.10.0")
    }
}
```

### 5c — Migrate `<dependencyManagement>` to a Gradle Platform

Maven's BOM-style `<dependencyManagement>` has two Gradle equivalents:

**Option A — Gradle Version Catalog** (recommended for new projects, Gradle 7.4+):

Create `gradle/libs.versions.toml`:

```toml
[versions]
spring-boot = "3.2.0"
junit = "5.10.0"

[libraries]
spring-boot-starter = { group = "org.springframework.boot", name = "spring-boot-starter", version.ref = "spring-boot" }
junit-jupiter = { group = "org.junit.jupiter", name = "junit-jupiter", version.ref = "junit" }

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
```

Then in each module's `build.gradle`:

```groovy
dependencies {
    implementation libs.spring.boot.starter
    testImplementation libs.junit.jupiter
}
```

**Option B — `platform()` / `enforcedPlatform()`** (for importing existing BOMs):

```groovy
dependencies {
    implementation platform('org.springframework.boot:spring-boot-dependencies:3.2.0')
    implementation 'org.springframework.boot:spring-boot-starter'  // no version needed
}
```

### 5d — Migrate `<properties>` to `gradle.properties` or `ext`

```groovy
// gradle.properties (key=value, available to all sub-projects)
appVersion=1.0.0
javaVersion=17

// OR in root build.gradle ext block:
ext {
    appVersion = '1.0.0'
    javaVersion = 17
}
```

---

## Step 6 — Handle Common Maven Plugin Migrations

See `references/api-reference.md` for the full plugin-mapping table. Key translations:

| Maven Plugin | Gradle Equivalent |
|---|---|
| `maven-compiler-plugin` | Built-in `java` plugin (`sourceCompatibility`, `targetCompatibility`) |
| `maven-surefire-plugin` | Built-in `test` task + JUnit Platform |
| `maven-failsafe-plugin` | Custom integration test source set or `test` task with custom filter |
| `maven-jar-plugin` | Built-in `jar` task |
| `maven-war-plugin` | `war` plugin |
| `maven-shade-plugin` | `com.github.johnrengelman.shadow` plugin |
| `spring-boot-maven-plugin` | `org.springframework.boot` Gradle plugin |
| `maven-checkstyle-plugin` | `checkstyle` plugin |
| `jacoco-maven-plugin` | `jacoco` plugin |
| `sonar-maven-plugin` | `org.sonarqube` Gradle plugin |
| `maven-release-plugin` | `axion-release` or `nebula-release` Gradle plugin |
| `exec-maven-plugin` | `application` plugin or custom `Exec` task |

**Maven Profiles → Gradle Conditional Logic:**

Maven profiles don't have a direct Gradle equivalent. Translate them to:

```groovy
// Use project properties (gradle -Penv=prod build)
if (project.hasProperty('env') && project.env == 'prod') {
    apply from: 'gradle/prod.gradle'
}

// Or use environment variables
if (System.getenv('CI')) {
    tasks.test {
        maxParallelForks = 4
    }
}
```

---

## Step 7 — Verify the Build

Run through these checks in order:

```bash
# 1. Check the project structure is recognized correctly
./gradlew projects

# 2. List all resolved dependencies (spot resolution conflicts)
./gradlew dependencies
# For a specific module in a multi-module build:
./gradlew :module-a:dependencies

# 3. Run unit tests
./gradlew test

# 4. Full build (compile + test + package)
./gradlew clean build

# 5. For multi-module: build a specific subproject
./gradlew :module-b:build
```

If the build succeeds and tests pass, the migration is functionally complete.

---

## Step 8 — Final Cleanup

1. **Keep `pom.xml` files** until the Gradle build is verified in CI.
2. **Add `/.gradle` and `/build` to `.gitignore`** (Gradle equivalents of Maven's `/target`).
3. **Remove `target/` entries** from `.gitignore` if they were Maven-only.
4. **Update CI/CD pipelines** — replace `mvn` commands with `./gradlew` equivalents:
   - `mvn clean install` → `./gradlew clean build`
   - `mvn test` → `./gradlew test`
   - `mvn verify -DskipITs=false` → `./gradlew integrationTest` (if configured)

---

## Common Pitfalls

- **Transitive dependency differences**: Gradle and Maven have different resolution strategies.
  Run `./gradlew dependencies` and compare against `mvn dependency:tree`.
- **Resource filtering**: Maven's `<filtering>true</filtering>` needs explicit `processResources`
  configuration in Gradle (use `expand` or `filter` in the `processResources` task).
- **Test exclusion patterns**: Surefire `<excludes>` become `test { exclude '**/*IT.class' }`.
- **Multi-module circular dependencies**: Gradle enforces DAG (no cycles). Maven allows some
  cases Gradle rejects. Refactor modules if `gradle projects` reports circular dependency errors.
- **Module naming**: Gradle module names use `:` separators (`:module-a:sub-module`).
  Directory names drive the module name unless overridden in `settings.gradle`.
- **Build cache**: Gradle's build cache is a feature, not a bug. Enable with
  `org.gradle.caching=true` in `gradle.properties` for faster CI builds.
- **Annotation processors**: Maven's `maven-compiler-plugin` annotation processor config
  becomes Gradle's `annotationProcessor` configuration. Lombok, MapStruct, etc. need
  explicit wiring.
