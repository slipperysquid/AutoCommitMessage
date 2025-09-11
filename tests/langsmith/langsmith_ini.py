# setup_project.py
import os
import uuid
from langsmith import Client
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
client = Client()


uid = uuid.uuid4()
project_name = f"commit-generator-{uid}"


client.create_project(
    project_name=project_name,
    description="A project that generates github commit messages automatically.",
)

print(f"Project '{project_name}' created successfully!")
# For convenience, you can print the export command
print("\nRun the following command in your terminal to set the project:")
print(f'export LANGCHAIN_PROJECT="{project_name}"')
