import os
import xml.etree.ElementTree as ET
import sys

def analyze_pom(pom_path):
    if not os.path.exists(pom_path):
        print(f"Error: {pom_path} not found.")
        return

    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        
        # Handle namespaces
        ns = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
        
        # Basic Info
        group_id = root.find('mvn:groupId', ns)
        artifact_id = root.find('mvn:artifactId', ns)
        version = root.find('mvn:version', ns)
        
        print(f"Project: {group_id.text if group_id is not None else 'N/A'}:{artifact_id.text if artifact_id is not None else 'N/A'}:{version.text if version is not None else 'N/A'}")
        
        # Modules (for multi-module projects)
        modules = root.find('mvn:modules', ns)
        if modules is not None:
            print("\nModules detected:")
            for module in modules.findall('mvn:module', ns):
                print(f" - {module.text}")
        
        # Plugins
        build = root.find('mvn:build', ns)
        if build is not None:
            plugins = build.find('mvn:plugins', ns)
            if plugins is not None:
                print("\nPlugins detected:")
                for plugin in plugins.findall('mvn:plugin', ns):
                    p_artifact = plugin.find('mvn:artifactId', ns)
                    if p_artifact is not None:
                        print(f" - {p_artifact.text}")

        # Profiles
        profiles = root.find('mvn:profiles', ns)
        if profiles is not None:
            print("\nProfiles detected (manual migration required for complex profiles):")
            for profile in profiles.findall('mvn:profile', ns):
                p_id = profile.find('mvn:id', ns)
                if p_id is not None:
                    print(f" - {p_id.text}")

    except Exception as e:
        print(f"Error parsing POM: {e}")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else 'pom.xml'
    analyze_pom(path)