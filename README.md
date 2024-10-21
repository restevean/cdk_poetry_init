# CDK Project Initializer with Poetry and Git

This Python script initializes a new AWS CDK (Cloud Development Kit) project using Poetry for dependency management (instead of venv) and Git for version control. This script names the project using the same name of the directory in which it is executed. Here's an overview of what the script does:

## What this script does when it's invoked

1. **Git Repository Setup**
   - Initializes a new Git repository in the current directory.

2. **Poetry Project Initialization**
   - Creates a new Poetry project with basic metadata.

3. **CDK Dependencies**
   - Adds AWS CDK libraries and pytest as dependencies.

4. **Project Structure Creation**
   - Creates necessary directories for the CDK project.

5. **Configuration Files**
   - Generates `cdk.json` with CDK-specific configurations.
   - Creates `pyproject.toml` for Poetry configuration.

6. **Core Project Files**
   - Creates `app.py` as the entry point for the CDK app.
   - Generates a basic CDK stack file.

7. **Test Setup**
   - Sets up a basic test structure with pytest.

8. **Git Configuration**
   - Creates a `.gitignore` file with common exclusions for Python and CDK projects.

9. **README Creation**
   - Generates a comprehensive README.md with project setup and usage instructions.

10. **Dependency Installation**
    - Installs project dependencies using Poetry.

11. **Initial Git Commit**
    - Stages all created files and makes an initial Git commit.


## Main Functions

### `run_command(command)`
- Executes shell commands and handles errors.

### `create_file(filename, content)`
- Creates a new file with the specified content.

### `create_readme(project_name)`
- Generates a README.md file with project information and instructions.

### `main()`
- The core function that orchestrates the project initialization process.

## Additional Features

- The script provides feedback throughout the initialization process.
- After completion, it offers instructions on how to start using the CDK project.
- There's an option to delete the initialization script after execution.

## Some considerations

It is recommended to configure Poetry to initialize the project with the Python version available in the active directory: `poetry config virtualenvs.prefer-active-python true`.
 If you use pyenv, this simplifies the configuration process of your project.

## Usage

To use this script:

1. Create a new directory for your CDK project.
2. Verify that the version of Python available in this directory, Poetry will initialize the project with this version.
3. Place this script in the new directory.
3. Make the script executable: `chmod +x cdk_poetry_init.py`
4. Run the script: `./cdk_poetry_init.py`

The result is a fully initialized CDK project with Poetry for dependency management and Git for version control, ready for development.
