import yaml
import re

# Read the environment.yml file
with open("environment.yml", "r") as file:
    env_data = yaml.safe_load(file)

# Extract the environment name and dependencies
env_name = env_data.get('name', 'myenv')
dependencies = env_data.get('dependencies', [])

# List to store all package dependencies (with versions)
packages = []

# Parse dependencies and add them to the list
for dep in dependencies:
    if isinstance(dep, str):  # For simple packages like 'numpy=1.21.0'
        packages.append(dep)
    elif isinstance(dep, dict):  # For dependencies with channels (e.g., {'pip': ['package==version']})
        if 'pip' in dep:
            for pip_package in dep['pip']:
                packages.append(pip_package)
        else:
            # Handle other dependencies with versions (e.g., conda packages)
            for pkg, version in dep.items():
                packages.append(f"{pkg}={version}")

# Write the requirements to a new requirements.txt file
with open("requirements.txt", "w") as file:
    file.write(f"# Generated from environment.yml: {env_name}\n")
    file.write("\n".join(packages))

print(f"requirements.txt has been generated with specific versions for {env_name} environment.")