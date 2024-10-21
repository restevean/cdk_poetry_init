#!/usr/bin/env python3
import os
import subprocess
import sys
import json


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(error.decode('utf-8'))
        sys.exit(1)
    return output.decode('utf-8')


def create_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Created {filename}")


def create_readme(project_name):
    readme_content = """# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. The initialization
process also creates a poetry-based virtualenv within this project, stored
under the `.venv` directory. To create the virtualenv it assumes that there is a
`python3` (or `python` for Windows) executable in your path with access to the
`poetry` package.

To manually create a virtualenv on MacOS and Linux:

    $ poetry install

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv:

    $ poetry shell

If you are on a Windows platform, you would activate the virtualenv like this:

    % poetry shell

Once the virtualenv is activated, you can install the required dependencies:

    $ poetry install

At this point you can now synthesize the CloudFormation template for this code.

    $ cdk synth

To add additional dependencies, for example other CDK libraries, just add
them to your `pyproject.toml` file and rerun the `poetry install` command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
"""
    create_file("README.md", readme_content)
    # print("Created README.md")


def main():
    project_name = os.path.basename(os.getcwd())

    # Initialize Git repository
    print("Initializing Git repository...")
    run_command("git init")

    # Initialize Poetry project
    print("Initializing Poetry project...")
    run_command(
        f"poetry init -n --name {project_name} --description 'An AWS CDK project' --author 'Your Name <your.email@example.com>'")

    # Add CDK dependencies
    print("Adding CDK dependencies...")
    run_command("poetry add aws-cdk-lib constructs")
    run_command("poetry add --group dev pytest")

    # Update pyproject.toml
    with open("pyproject.toml", "a") as f:
        f.write(f"\npackages = [{{include = \"{project_name}\"}}]\n")

    # Create project structure
    os.makedirs(project_name)
    os.makedirs("tests/unit", exist_ok=True)

    # Create cdk.json
    cdk_json_content = {
        "app": f"poetry run python app.py",
        "watch": {
            "include": [
                "**"
            ],
            "exclude": [
                "README.md",
                "cdk*.json",
                "requirements*.txt",
                "source.bat",
                "**/__init__.py",
                "python/__pycache__",
                "tests"
            ]
        },
        "context": {
            "@aws-cdk/aws-lambda:recognizeLayerVersion": True,
            "@aws-cdk/core:checkSecretUsage": True,
            "@aws-cdk/core:target-partitions": [
                "aws",
                "aws-cn"
            ],
            "@aws-cdk-containers/ecs-service-extensions:enableDefaultLogDriver": True,
            "@aws-cdk/aws-ec2:uniqueImdsv2TemplateName": True,
            "@aws-cdk/aws-ecs:arnFormatIncludesClusterName": True,
            "@aws-cdk/aws-iam:minimizePolicies": True,
            "@aws-cdk/core:validateSnapshotRemovalPolicy": True,
            "@aws-cdk/aws-codepipeline:crossAccountKeyAliasStackSafeResourceName": True,
            "@aws-cdk/aws-s3:createDefaultLoggingPolicy": True,
            "@aws-cdk/aws-sns-subscriptions:restrictSqsDescryption": True,
            "@aws-cdk/aws-apigateway:disableCloudWatchRole": True,
            "@aws-cdk/core:enablePartitionLiterals": True,
            "@aws-cdk/aws-events:eventsTargetQueueSameAccount": True,
            "@aws-cdk/aws-iam:standardizedServicePrincipals": True,
            "@aws-cdk/aws-ecs:disableExplicitDeploymentControllerForCircuitBreaker": True,
            "@aws-cdk/aws-iam:importedRoleStackSafeDefaultPolicyName": True,
            "@aws-cdk/aws-s3:serverAccessLogsUseBucketPolicy": True,
            "@aws-cdk/aws-route53-patters:useCertificate": True,
            "@aws-cdk/customresources:installLatestAwsSdkDefault": False,
            "@aws-cdk/aws-rds:databaseProxyUniqueResourceName": True,
            "@aws-cdk/aws-codedeploy:removeAlarmsFromDeploymentGroup": True,
            "@aws-cdk/aws-apigateway:authorizerChangeDeploymentLogicalId": True,
            "@aws-cdk/aws-ec2:launchTemplateDefaultUserData": True,
            "@aws-cdk/aws-secretsmanager:useAttachedSecretResourcePolicy": True,
            "@aws-cdk/aws-redshift:columnId": True,
            "@aws-cdk/aws-stepfunctions-tasks:enableEmrServicePolicyV2": True,
            "@aws-cdk/aws-ec2:restrictDefaultSecurityGroup": True,
            "@aws-cdk/aws-apigateway:requestValidatorUniqueId": True
        }
    }
    create_file("cdk.json", json.dumps(cdk_json_content, indent=2))

    # Create app.py
    app_py_content = f"""#!/usr/bin/env python3
import os

import aws_cdk as cdk

from {project_name}.{project_name}_stack import {project_name.capitalize()}Stack


app = cdk.App()
{project_name.capitalize()}Stack(app, "{project_name.capitalize()}Stack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
"""
    create_file("app.py", app_py_content)

    # Create stack file
    stack_py_content = f"""from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class {project_name.capitalize()}Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "{project_name}Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
"""
    create_file(f"{project_name}/{project_name}_stack.py", stack_py_content)

    # Create __init__.py in project directory
    create_file(f"{project_name}/__init__.py", "")

    # Create __init__.py in tests directory
    create_file("tests/__init__.py", "")

    # Create __init__.py in tests/unit directory
    create_file("tests/unit/__init__.py", "")

    # Create tests/unit/test_cdk_project_stack.py
    test_content = f"""import aws_cdk as core
import aws_cdk.assertions as assertions

from {project_name}.{project_name}_stack import {project_name.capitalize()}Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in {project_name}/{project_name}_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = {project_name.capitalize()}Stack(app, "cdk-project")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {{
#         "VisibilityTimeout": 300
#     }})
"""
    create_file("tests/unit/test_cdk_project_stack.py", test_content)

    # Create .gitignore
    gitignore_content = """*.swp
package-lock.json
__pycache__
.pytest_cache
.venv
*.egg-info
.idea

# CDK asset staging directory
.cdk.staging
cdk.out
"""
    create_file(".gitignore", gitignore_content)

    # Create README.md
    create_readme(project_name)

    # Install dependencies
    print("Installing dependencies...")
    run_command("poetry install")

    # Initial git commit
    print("Creating initial Git commit...")
    run_command("git add .")
    run_command("git commit -m 'Initial commit'")

    print(f"\nCDK project '{project_name}' has been initialized with Poetry and Git!")
    print("To get started:")
    print("  poetry shell")
    print("  cdk synth")


if __name__ == "__main__":
    main()

    answer = input("Do you want to delete this script? (Y/N): ")

    if answer.lower() == 'y':
        script_path = __file__
        print(f"Deleting the file: {script_path}")
        os.remove(script_path)
    else:
        print("The script will not be deleted.")

"""
This updated script now includes:
Git initialization (git init)
Creation of a .gitignore file with common Python and CDK-specific entries
An initial Git commit with all the created files
To use this script:

Create a new directory for your project and navigate into it:

mkdir my-cdk-project
cd my-cdk-project

Save the script as cdk_poetry_init.py in this directory.

Make the script executable:
chmod +x cdk_poetry_init.py

Run the script:
./cdk_poetry_init.py
"""