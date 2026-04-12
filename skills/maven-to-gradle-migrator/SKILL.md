---
name: maven-to-gradle-migrator
description: "Automate the migration of Java Maven repositories to Java Gradle repositories. Use for: converting pom.xml to build.gradle, handling multi-module Maven projects, and verifying the Gradle build."
---

# Maven to Gradle Migrator

This skill provides a structured workflow for migrating Java projects from Maven to Gradle, ensuring dependency integrity and build stability.

## Prerequisites

- `java` and `gradle` must be installed in the environment.
- Access to the Maven repository (containing `pom.xml`).

## Migration Workflow

### 1. Analyze the Maven Project
Before migrating, analyze the existing Maven structure to identify potential complexities like multi-module setups, custom plugins, or profiles.

```bash
python /home/ubuntu/skills/maven-to-gradle-migrator/scripts/analyze_maven.py [path/to/pom.xml]
```

### 2. Run Automatic Conversion
Use the Gradle `init` plugin to perform the initial conversion. This handles basic dependency mapping and project structure.

```bash
# In the root directory of the Maven project
gradle init --type pom
```

### 3. Handle Multi-Module Projects
If the Maven project has sub-modules, ensure `settings.gradle` correctly includes all sub-projects. The `gradle init` command usually handles this, but verify the output.

### 4. Manual Refinement
Check for common migration issues:
- **Profiles**: Maven profiles do not have a direct 1:1 equivalent in Gradle. Use Gradle's conditional logic in `build.gradle` or separate build files.
- **Plugins**: Replace Maven plugins with their Gradle equivalents (e.g., `maven-compiler-plugin` -> `java` plugin).
- **Custom Properties**: Migrate `<properties>` from `pom.xml` to `gradle.properties` or `ext` blocks in `build.gradle`.

### 5. Verify the Build
Run the Gradle build and tests to ensure the migration was successful.

```bash
./gradlew clean build
```

## Best Practices

- **Keep `pom.xml` temporarily**: Do not delete the `pom.xml` until the Gradle build is fully verified.
- **Use the Gradle Wrapper**: Always use `./gradlew` to ensure build reproducibility.
- **Check Dependency Constraints**: Maven's `<dependencyManagement>` should be migrated to Gradle's `platform()` or `enforcedPlatform()`.

## Common Pitfalls

- **Transitive Dependency Resolution**: Gradle and Maven may resolve transitive dependencies differently. Use `./gradlew dependencies` to compare.
- **Resource Filtering**: Maven's resource filtering needs to be manually configured in Gradle's `processResources` task.
- **Test Exclusions**: Ensure any `<excludes>` in Maven's Surefire plugin are migrated to Gradle's `test` task configuration.