#!/usr/bin/env python3
"""
analyze_maven.py — Analyze a Maven project (single or multi-module) before Gradle migration.

Usage:
    python analyze_maven.py [path/to/pom.xml]

Recursively walks sub-modules and reports:
  - Project coordinates (groupId:artifactId:version)
  - Module hierarchy
  - Declared plugins per module
  - Maven profiles per module
  - <dependencyManagement> entries (BOM/platform candidates)
  - Direct dependencies per module
  - <properties> used across the project
  - Potential migration warnings
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
INDENT = "  "

# ─────────────────────────── helpers ────────────────────────────────────────

def tag(name):
    return f"{{{NS['mvn']}}}{name}"


def find(elem, *path):
    """Walk a dotted tag path and return the element, or None."""
    cur = elem
    for p in path:
        if cur is None:
            return None
        cur = cur.find(f"mvn:{p}", NS)
    return cur


def text_of(elem, *path):
    node = find(elem, *path)
    return node.text.strip() if node is not None and node.text else None


def parse_pom(pom_path):
    try:
        tree = ET.parse(pom_path)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"  [ERROR] Cannot parse {pom_path}: {e}")
        return None


# ─────────────────────────── per-pom extraction ─────────────────────────────

def extract_coordinates(root, parent_coords=None):
    """Return (groupId, artifactId, version) inheriting from parent where needed."""
    group = text_of(root, 'groupId') or (parent_coords[0] if parent_coords else 'N/A')
    artifact = text_of(root, 'artifactId') or 'N/A'
    version = text_of(root, 'version') or (parent_coords[2] if parent_coords else 'N/A')
    return group, artifact, version


def extract_modules(root):
    modules_node = find(root, 'modules')
    if modules_node is None:
        return []
    return [m.text.strip() for m in modules_node.findall(f"mvn:module", NS) if m.text]


def extract_plugins(root):
    plugins = []
    for section in ['build/plugins', 'build/pluginManagement/plugins']:
        parts = section.split('/')
        node = find(root, *parts)
        if node is None:
            continue
        for plugin in node.findall(f"mvn:plugin", NS):
            g = text_of(plugin, 'groupId') or 'org.apache.maven.plugins'
            a = text_of(plugin, 'artifactId') or '?'
            v = text_of(plugin, 'version') or '(inherited)'
            plugins.append(f"{g}:{a}:{v}")
    return plugins


def extract_profiles(root):
    profiles_node = find(root, 'profiles')
    if profiles_node is None:
        return []
    results = []
    for p in profiles_node.findall(f"mvn:profile", NS):
        pid = text_of(p, 'id') or '(unnamed)'
        activation = find(p, 'activation')
        hint = ''
        if activation is not None:
            ad = text_of(activation, 'activeByDefault')
            prop = text_of(activation, 'property', 'name')
            if ad == 'true':
                hint = ' [activeByDefault]'
            elif prop:
                hint = f' [activated by property: {prop}]'
        results.append(f"{pid}{hint}")
    return results


def extract_dependency_management(root):
    dm = find(root, 'dependencyManagement', 'dependencies')
    if dm is None:
        return []
    deps = []
    for dep in dm.findall(f"mvn:dependency", NS):
        g = text_of(dep, 'groupId') or '?'
        a = text_of(dep, 'artifactId') or '?'
        v = text_of(dep, 'version') or '(managed)'
        scope = text_of(dep, 'scope') or ''
        dep_type = text_of(dep, 'type') or ''
        extra = ', '.join(filter(None, [scope, dep_type]))
        deps.append(f"{g}:{a}:{v}" + (f" [{extra}]" if extra else ""))
    return deps


def extract_dependencies(root):
    node = find(root, 'dependencies')
    if node is None:
        return []
    deps = []
    for dep in node.findall(f"mvn:dependency", NS):
        g = text_of(dep, 'groupId') or '?'
        a = text_of(dep, 'artifactId') or '?'
        v = text_of(dep, 'version') or '(managed)'
        scope = text_of(dep, 'scope') or 'compile'
        deps.append(f"{g}:{a}:{v} [scope={scope}]")
    return deps


def extract_properties(root):
    node = find(root, 'properties')
    if node is None:
        return {}
    return {child.tag.split('}')[-1]: (child.text or '').strip()
            for child in node}


# ─────────────────────────── warnings ───────────────────────────────────────

def generate_warnings(plugins, profiles, dep_management, dependencies):
    warnings = []
    plugin_ids = [p.split(':')[1] for p in plugins]

    tricky_plugins = {
        'maven-shade-plugin': 'Use com.github.johnrengelman.shadow in Gradle',
        'maven-assembly-plugin': 'Use distribution plugin or shadow plugin',
        'maven-release-plugin': 'Use axion-release or nebula-release Gradle plugin',
        'exec-maven-plugin': 'Use application plugin or custom Exec task',
        'build-helper-maven-plugin': 'Use custom source sets in Gradle',
        'maven-antrun-plugin': 'Rewrite as Gradle Exec or JavaExec task',
        'cobertura-maven-plugin': 'Use jacoco plugin',
        'findbugs-maven-plugin': 'Use spotbugs-gradle-plugin',
    }
    for pid, hint in tricky_plugins.items():
        if pid in plugin_ids:
            warnings.append(f"Plugin '{pid}' needs manual migration: {hint}")

    if profiles:
        warnings.append(
            f"{len(profiles)} Maven profile(s) detected — no direct Gradle equivalent; "
            "translate to property-based conditions or separate build files"
        )

    bom_entries = [d for d in dep_management if '[pom,' in d or 'import' in d.lower()]
    if bom_entries:
        warnings.append(
            f"{len(bom_entries)} BOM import(s) in dependencyManagement — "
            "use platform() or enforcedPlatform() in Gradle, or a version catalog"
        )

    annotation_processors = ['lombok', 'mapstruct', 'dagger']
    dep_artifacts = [d.split(':')[1].lower() for d in dependencies]
    for ap in annotation_processors:
        if any(ap in a for a in dep_artifacts):
            warnings.append(
                f"Annotation processor '{ap}' detected — add to 'annotationProcessor' "
                "configuration in Gradle (not just 'implementation')"
            )

    return warnings


# ─────────────────────────── recursive walker ───────────────────────────────

def analyze_pom(pom_path, depth=0, parent_coords=None, all_properties=None):
    """Analyze one POM and recursively descend into sub-modules."""
    if all_properties is None:
        all_properties = {}

    pom_path = Path(pom_path).resolve()
    if not pom_path.exists():
        print(f"{INDENT * depth}[MISSING] {pom_path}")
        return

    root = parse_pom(pom_path)
    if root is None:
        return

    coords = extract_coordinates(root, parent_coords)
    modules = extract_modules(root)
    plugins = extract_plugins(root)
    profiles = extract_profiles(root)
    dep_mgmt = extract_dependency_management(root)
    dependencies = extract_dependencies(root)
    properties = extract_properties(root)
    warnings = generate_warnings(plugins, profiles, dep_mgmt, dependencies)

    # Merge properties upward for reporting
    all_properties.update(properties)

    prefix = INDENT * depth
    is_root = depth == 0

    print(f"\n{'═' * 60}" if is_root else f"\n{prefix}{'─' * (58 - depth * 2)}")
    print(f"{prefix}{'📦 ' if is_root else '📁 '}Module: {':'.join(coords)}")
    print(f"{prefix}   Path: {pom_path.parent}")

    if modules:
        print(f"{prefix}   Sub-modules ({len(modules)}): {', '.join(modules)}")

    if plugins:
        print(f"{prefix}   Plugins ({len(plugins)}):")
        for p in plugins:
            print(f"{prefix}     · {p}")

    if profiles:
        print(f"{prefix}   Profiles ({len(profiles)}):")
        for p in profiles:
            print(f"{prefix}     · {p}")

    if dep_mgmt:
        print(f"{prefix}   Managed dependencies ({len(dep_mgmt)}):")
        for d in dep_mgmt:
            print(f"{prefix}     · {d}")

    if dependencies:
        print(f"{prefix}   Direct dependencies ({len(dependencies)}):")
        for d in dependencies:
            print(f"{prefix}     · {d}")

    if properties and is_root:
        print(f"{prefix}   Properties ({len(properties)}):")
        for k, v in sorted(properties.items()):
            print(f"{prefix}     {k} = {v}")

    if warnings:
        print(f"{prefix}   ⚠️  Migration warnings:")
        for w in warnings:
            print(f"{prefix}     ! {w}")

    # Recurse into sub-modules
    base_dir = pom_path.parent
    for module in modules:
        module_pom = base_dir / module / 'pom.xml'
        analyze_pom(module_pom, depth=depth + 1, parent_coords=coords,
                    all_properties=all_properties)


# ─────────────────────────── entrypoint ─────────────────────────────────────

def main():
    pom_path = sys.argv[1] if len(sys.argv) > 1 else 'pom.xml'

    print("Maven Project Analyzer — Pre-Migration Report")
    print("=" * 60)
    print(f"Root POM: {Path(pom_path).resolve()}\n")

    all_properties = {}
    analyze_pom(pom_path, all_properties=all_properties)

    print(f"\n{'═' * 60}")
    print("✅ Analysis complete. Review warnings above before migrating.")
    print("   Next step: gradle init --type pom --dsl groovy")
    print("=" * 60)


if __name__ == "__main__":
    main()
