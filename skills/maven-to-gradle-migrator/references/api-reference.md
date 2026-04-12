# Maven → Gradle Reference

Full translation tables and code snippets for converting Maven concepts to Gradle.
Read this file when you need the Gradle equivalent of a specific Maven feature.

---

## Table of Contents

1. [Project Coordinates](#1-project-coordinates)
2. [Multi-Module Structure](#2-multi-module-structure)
3. [Dependency Scopes](#3-dependency-scopes)
4. [Dependency Management / BOMs](#4-dependency-management--boms)
5. [Common Plugin Translations](#5-common-plugin-translations)
6. [Build Lifecycle → Gradle Tasks](#6-build-lifecycle--gradle-tasks)
7. [Properties and Variables](#7-properties-and-variables)
8. [Profiles → Conditional Logic](#8-profiles--conditional-logic)
9. [Repositories](#9-repositories)
10. [Annotation Processors](#10-annotation-processors)
11. [Resource Filtering](#11-resource-filtering)
12. [Integration Tests](#12-integration-tests)
13. [Version Catalog (Gradle 7.4+)](#13-version-catalog-gradle-74)

---

## 1. Project Coordinates

**Maven (`pom.xml`)**
```xml
<groupId>com.example</groupId>
<artifactId>my-app</artifactId>
<version>1.0.0-SNAPSHOT</version>
<packaging>jar</packaging>
```

**Gradle (Groovy DSL)**
```groovy
group = 'com.example'
version = '1.0.0-SNAPSHOT'
// 'jar' is the default; for war use: apply plugin: 'war'
```

**Gradle (Kotlin DSL)**
```kotlin
group = "com.example"
version = "1.0.0-SNAPSHOT"
```

---

## 2. Multi-Module Structure

### Maven root `pom.xml`
```xml
<modules>
  <module>module-api</module>
  <module>module-service</module>
  <module>module-web</module>
  <module>module-service/sub-module</module>  <!-- nested -->
</modules>
```

### Gradle `settings.gradle` (Groovy)
```groovy
rootProject.name = 'my-project'

include 'module-api'
include 'module-service'
include 'module-web'
include 'module-service:sub-module'   // nested uses colon, not slash
```

### Gradle `settings.gradle.kts` (Kotlin)
```kotlin
rootProject.name = "my-project"

include("module-api", "module-service", "module-web")
include("module-service:sub-module")
```

### Shared config in root `build.gradle` (replaces parent POM `<build>`)
```groovy
subprojects {
    apply plugin: 'java'
    apply plugin: 'java-library'  // if modules expose APIs

    java {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    repositories {
        mavenCentral()
        maven { url 'https://repo.example.com/maven2' }
    }

    // Common test dependency for all modules
    dependencies {
        testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
        testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
    }

    test {
        useJUnitPlatform()
    }
}

// Config only for the root project itself (not sub-projects)
// allprojects { } would apply to root AND sub-projects
```

### Inter-module dependencies
Maven `<dependency>` on a sibling module:
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>module-api</artifactId>
    <version>${project.version}</version>
</dependency>
```

Gradle equivalent (use project reference, not coordinates):
```groovy
dependencies {
    implementation project(':module-api')
}
```

---

## 3. Dependency Scopes

| Maven Scope | Gradle Configuration | Notes |
|---|---|---|
| `compile` (default) | `implementation` | Not exported to consumers |
| `compile` (exported) | `api` | Requires `java-library` plugin |
| `provided` | `compileOnly` | Not on runtime classpath |
| `runtime` | `runtimeOnly` | Not on compile classpath |
| `test` | `testImplementation` | Test compile + runtime |
| `test` (runtime only) | `testRuntimeOnly` | e.g., JUnit launcher |
| `system` | Avoid — use local file dependencies instead |
| `import` (in `<dependencyManagement>`) | `platform()` or `enforcedPlatform()` |

---

## 4. Dependency Management / BOMs

### Maven `<dependencyManagement>`
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.2.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Gradle `platform()` equivalent
```groovy
dependencies {
    implementation platform('org.springframework.boot:spring-boot-dependencies:3.2.0')
    // Now you can omit versions for Spring Boot managed deps:
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

### `enforcedPlatform()` (forces versions, overrides transitive)
```groovy
dependencies {
    implementation enforcedPlatform('org.springframework.boot:spring-boot-dependencies:3.2.0')
}
```

---

## 5. Common Plugin Translations

### `maven-compiler-plugin`
```xml
<plugin>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <source>17</source>
        <target>17</target>
        <encoding>UTF-8</encoding>
    </configuration>
</plugin>
```
↓
```groovy
java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}
compileJava.options.encoding = 'UTF-8'
```

### `maven-surefire-plugin` (unit tests)
```xml
<plugin>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <includes><include>**/*Test.java</include></includes>
        <excludes><exclude>**/*IT.java</exclude></excludes>
    </configuration>
</plugin>
```
↓
```groovy
test {
    useJUnitPlatform()
    include '**/*Test.class'
    exclude '**/*IT.class'
}
```

### `maven-failsafe-plugin` (integration tests)
```groovy
// Define a separate source set
sourceSets {
    integrationTest {
        java.srcDir 'src/integration-test/java'
        resources.srcDir 'src/integration-test/resources'
        compileClasspath += sourceSets.main.output + configurations.testRuntimeClasspath
        runtimeClasspath += output + compileClasspath
    }
}

configurations {
    integrationTestImplementation.extendsFrom testImplementation
    integrationTestRuntimeOnly.extendsFrom testRuntimeOnly
}

tasks.register('integrationTest', Test) {
    description = 'Runs integration tests.'
    group = 'verification'
    testClassesDirs = sourceSets.integrationTest.output.classesDirs
    classpath = sourceSets.integrationTest.runtimeClasspath
    useJUnitPlatform()
    include '**/*IT.class'
    shouldRunAfter test
}
check.dependsOn integrationTest
```

### `maven-shade-plugin` → Shadow plugin
```groovy
// build.gradle
plugins {
    id 'com.github.johnrengelman.shadow' version '8.1.1'
}

shadowJar {
    archiveClassifier = ''  // replaces the default jar
    mergeServiceFiles()
}
```

### `spring-boot-maven-plugin`
```groovy
plugins {
    id 'org.springframework.boot' version '3.2.0'
    id 'io.spring.dependency-management' version '1.1.4'
}

// bootJar / bootRun tasks are added automatically
bootJar {
    archiveFileName = 'app.jar'
}
```

### `maven-checkstyle-plugin`
```groovy
plugins {
    id 'checkstyle'
}

checkstyle {
    toolVersion = '10.12.4'
    configFile = file('config/checkstyle/checkstyle.xml')
}
```

### `jacoco-maven-plugin`
```groovy
plugins {
    id 'jacoco'
}

jacocoTestReport {
    dependsOn test
    reports {
        xml.required = true
        html.required = true
    }
}

jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit {
                minimum = 0.80  // 80% minimum coverage
            }
        }
    }
}
check.dependsOn jacocoTestCoverageVerification
```

### `sonar-maven-plugin` → SonarQube Gradle plugin
```groovy
plugins {
    id 'org.sonarqube' version '4.4.1.3373'
}

sonar {
    properties {
        property 'sonar.projectKey', 'my-project'
        property 'sonar.host.url', 'https://sonar.example.com'
    }
}
```

### `maven-release-plugin` → axion-release
```groovy
plugins {
    id 'pl.allegro.tech.build.axion-release' version '1.17.0'
}

project.version = scmVersion.version
```

### `exec-maven-plugin`
```groovy
tasks.register('runApp', JavaExec) {
    classpath = sourceSets.main.runtimeClasspath
    mainClass = 'com.example.Main'
    args = ['arg1', 'arg2']
}
```

### `maven-war-plugin`
```groovy
plugins {
    id 'war'
}

war {
    archiveFileName = 'app.war'
    webAppDirectory = file('src/main/webapp')
}
```

### `maven-jar-plugin` (custom manifest)
```groovy
jar {
    manifest {
        attributes(
            'Main-Class': 'com.example.Main',
            'Implementation-Version': version
        )
    }
    archiveClassifier = ''  // override default 'plain' suffix if using Spring Boot
}
```

---

## 6. Build Lifecycle → Gradle Tasks

| Maven Phase | Gradle Task Equivalent |
|---|---|
| `mvn clean` | `./gradlew clean` |
| `mvn compile` | `./gradlew compileJava` |
| `mvn test` | `./gradlew test` |
| `mvn package` | `./gradlew jar` or `./gradlew war` |
| `mvn verify` | `./gradlew check` |
| `mvn install` | `./gradlew publishToMavenLocal` |
| `mvn deploy` | `./gradlew publish` (requires `maven-publish` plugin) |
| `mvn clean install` | `./gradlew clean build` |
| `mvn clean install -DskipTests` | `./gradlew clean build -x test` |
| `mvn dependency:tree` | `./gradlew dependencies` |
| `mvn sonar:sonar` | `./gradlew sonar` |

---

## 7. Properties and Variables

### Maven `<properties>`
```xml
<properties>
    <java.version>17</java.version>
    <spring.version>3.2.0</spring.version>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
```

### Gradle `gradle.properties` (project-wide, all sub-projects)
```properties
# gradle.properties
javaVersion=17
springVersion=3.2.0
org.gradle.jvmargs=-Xmx2g -XX:+HeapDumpOnOutOfMemoryError
org.gradle.caching=true
```

### Gradle `ext` block (in `build.gradle`)
```groovy
ext {
    javaVersion = 17
    springVersion = '3.2.0'
}

// Reference in same or sub-projects:
dependencies {
    implementation "org.springframework.boot:spring-boot-starter:${rootProject.ext.springVersion}"
}
```

---

## 8. Profiles → Conditional Logic

Maven profiles have no direct Gradle equivalent. Map them to:

### Property-based condition
```groovy
// Run with: ./gradlew build -Penv=production
if (project.hasProperty('env') && project.env == 'production') {
    println "Production build"
    // apply production-specific config
}
```

### Environment variable condition
```groovy
if (System.getenv('CI')) {
    test { maxParallelForks = Runtime.runtime.availableProcessors() }
}
```

### Separate script files (for complex profiles)
```groovy
// Root build.gradle
if (project.hasProperty('profile')) {
    apply from: "gradle/${project.profile}.gradle"
}
```

```groovy
// gradle/production.gradle
dependencies {
    runtimeOnly 'com.h2database:h2'  // different DB for prod
}
```

---

## 9. Repositories

```groovy
repositories {
    mavenCentral()          // replaces <repository>central
    mavenLocal()            // replaces localRepository (~/.m2)
    maven {
        url 'https://repo.example.com/maven2'
        credentials {
            username = project.findProperty('repoUser') ?: System.getenv('REPO_USER')
            password = project.findProperty('repoPass') ?: System.getenv('REPO_PASS')
        }
    }
}
```

---

## 10. Annotation Processors

Maven handles annotation processors through the compiler plugin. Gradle requires explicit configuration.

```groovy
dependencies {
    // Lombok
    compileOnly 'org.projectlombok:lombok:1.18.30'
    annotationProcessor 'org.projectlombok:lombok:1.18.30'
    testCompileOnly 'org.projectlombok:lombok:1.18.30'
    testAnnotationProcessor 'org.projectlombok:lombok:1.18.30'

    // MapStruct
    implementation 'org.mapstruct:mapstruct:1.5.5.Final'
    annotationProcessor 'org.mapstruct:mapstruct-processor:1.5.5.Final'

    // If using Lombok + MapStruct together, order matters:
    annotationProcessor 'org.projectlombok:lombok-mapstruct-binding:0.2.0'
}
```

---

## 11. Resource Filtering

Maven's `<filtering>true</filtering>` expands `${property}` in resource files. In Gradle:

```groovy
processResources {
    filesMatching('**/*.properties') {
        expand(project.properties)
    }
    // Or expand a specific map:
    filesMatching('application.properties') {
        expand([
            version: project.version,
            buildDate: new Date().format('yyyy-MM-dd')
        ])
    }
}
```

---

## 12. Integration Tests

See the `maven-failsafe-plugin` section above for the full source set setup. Quick reference:

```bash
# Run all tests (unit + integration)
./gradlew check

# Run only unit tests
./gradlew test

# Run only integration tests
./gradlew integrationTest
```

---

## 13. Version Catalog (Gradle 7.4+)

The recommended way to centralize dependency versions in a multi-module Gradle project (replaces Maven's `<dependencyManagement>`).

### `gradle/libs.versions.toml`
```toml
[versions]
spring-boot = "3.2.0"
junit = "5.10.0"
lombok = "1.18.30"
mapstruct = "1.5.5.Final"

[libraries]
spring-boot-starter = { group = "org.springframework.boot", name = "spring-boot-starter", version.ref = "spring-boot" }
spring-boot-starter-web = { group = "org.springframework.boot", name = "spring-boot-starter-web", version.ref = "spring-boot" }
spring-boot-starter-test = { group = "org.springframework.boot", name = "spring-boot-starter-test", version.ref = "spring-boot" }
junit-jupiter = { group = "org.junit.jupiter", name = "junit-jupiter", version.ref = "junit" }
lombok = { group = "org.projectlombok", name = "lombok", version.ref = "lombok" }
mapstruct = { group = "org.mapstruct", name = "mapstruct", version.ref = "mapstruct" }
mapstruct-processor = { group = "org.mapstruct", name = "mapstruct-processor", version.ref = "mapstruct" }

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
spring-dependency-management = { id = "io.spring.dependency-management", version = "1.1.4" }
```

### Usage in a sub-module `build.gradle`
```groovy
dependencies {
    implementation libs.spring.boot.starter.web
    compileOnly libs.lombok
    annotationProcessor libs.lombok
    testImplementation libs.spring.boot.starter.test
    testImplementation libs.junit.jupiter
}
```

### Usage in a sub-module `build.gradle.kts`
```kotlin
dependencies {
    implementation(libs.spring.boot.starter.web)
    compileOnly(libs.lombok)
    annotationProcessor(libs.lombok)
    testImplementation(libs.spring.boot.starter.test)
    testImplementation(libs.junit.jupiter)
}
```
