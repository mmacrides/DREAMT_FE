import yaml
import os

# Load the YAML file
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Generate the requirements.txt for pip
def generate_pip_requirements(env_data):
    pip_requirements = []
    
    for dep in env_data.get('dependencies', []):
        if isinstance(dep, dict):  # If it's a conda package with specific channels
            for key, value in dep.items():
                if key == 'pip':
                    # If there is a 'pip' section, add the packages to pip_requirements
                    pip_requirements.extend(value)
        elif isinstance(dep, str):  # Normal package declaration
            # Conda-specific entries like '_libgcc_mutex' and '_openmp_mutex' are skipped
            if '=' in dep:
                dep = dep.split('=')[0]  # Keep only the package name
            # Skip Conda-specific packages that aren't compatible with pip
            if dep not in ['_libgcc_mutex', '_openmp_mutex', 'conda', 'pip', 'backports', 'backports.functools_lru_cache']:
                pip_requirements.append(dep)
    
    return pip_requirements

# Generate the conda_requirements.txt (including all Conda dependencies)
def generate_conda_requirements(env_data):
    conda_requirements = []
    
    for dep in env_data.get('dependencies', []):
        if isinstance(dep, dict):
            for key, value in dep.items():
                if key == 'pip':
                    conda_requirements.append('pip:')
                    conda_requirements.extend(value)
                else:
                    conda_requirements.append(f"{key}={value}")
        elif isinstance(dep, str):
            conda_requirements.append(dep)
    
    return conda_requirements

# Save the requirements to a file
def save_requirements(requirements, filename):
    with open(filename, 'w') as file:
        for req in requirements:
            file.write(f"{req}\n")

# Main function to convert env file to pip and conda requirements
def convert_to_requirements(env_file_path):
    # Load environment YAML file
    env_data = load_yaml(env_file_path)
    
    # Generate pip requirements and conda requirements
    pip_requirements = generate_pip_requirements(env_data)
    conda_requirements = generate_conda_requirements(env_data)
    
    # Create a directory for conda requirements if not exists
    os.makedirs('conda_requirements', exist_ok=True)
    
    # Save requirements to the corresponding files
    save_requirements(pip_requirements, 'requirements.txt')
    save_requirements(conda_requirements, 'conda_requirements/conda_requirements.txt')

# Run the conversion
convert_to_requirements('environment.yml')

print("Requirements have been generated.")