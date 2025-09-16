# AutoCommitMessage

AutoCommitMessage is a command-line tool that uses the power of Large Language Models (LLMs) to automatically generate descriptive and well-formatted git commit messages based on your staged changes.

## Features

* **AI-Powered Commits:** Leverages Google's Gemini models via LangChain to analyze your code differences and generate meaningful commit messages.
* **Free to Use:** This tool includes a wrapper around the Google API to ensure that your usage stays within the free tier, so you can use it without charge with your own Google API key.
* **Conventional Commits:** Follows the Conventional Commits specification to produce a clean and readable commit history. The generated messages include a type (e.g., `feat`, `fix`, `refactor`), an optional scope, and a concise description.
* **Seamless Git Integration:** Integrates directly with your local Git repository to automatically detect staged files.
* **Extensible and Testable:** Built with a modular structure, making it easy to test and extend. The project includes unit, end-to-end, and LLM quality tests.

## Installation

1.  **Install from PyPI (Recommended):**
    You can install the tool directly using pip.
    ```bash
    pip install autocommitmessage
    ```

2.  **Or, Install from source (for development):**
    If you want to contribute to the project, you can install it from the source code.

    * **Clone the repository:**
        ```bash
        git clone <your-repo-url>
        cd autocommitmessage
        ```

    * **Install dependencies:**
        The project uses `setuptools` for packaging. It's recommended to do this in a virtual environment.
        ```bash
        pip install .
        ```
        For development and running tests, install the testing dependencies:
        ```bash
        pip install .[dev]
        ```

## Usage

After installing, you can use `autocommitmessage` in any of your own Git repositories.

### Setting Your API Key

The tool requires a Google API key to function. You must set this key in a `.env` file within the root directory of the repository you are working on.

1.  **Navigate to your project's root directory:**
    ```bash
    cd /path/to/your-project
    ```
2.  **Create a `.env` file.** If you cloned the repository for development, you can copy the example file:
    ```bash
    cp .env.example .env
    ```
    Then, add your API key:
    ```
    # your-project/.env
    GOOGLE_API_KEY="your_google_api_key_here"
    ```

### Generating a Commit Message

1.  **Stage your changes:**
    Use `git add` to stage the changes you want to commit.
    ```bash
    git add <file1> <file2>
    ```

2.  **Generate the commit message:**
    Run the `autocommitmessage` command.
    ```bash
    autocommitmessage
    ```

The tool will then output a generated commit message based on the staged diff.

## Development and Testing

If you are contributing to the project, you will need to set up your environment for testing.

### Langsmith Setup (for LLM Quality Tests)

1.  **Add Langsmith keys to your `.env` file:**
    ```
    LANGCHAIN_API_KEY="your_langchain_api_key"
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
    LANGCHAIN_PROJECT="your_project_name"
    ```
2.  You can get the `LANGCHAIN_PROJECT` name by running the `langsmith_ini.py` script:
    ```bash
    python tests/langsmith/langsmith_ini.py
    ```

### Running Tests

This project uses `pytest` for testing. The tests are organized into three categories: unit, end-to-end (`e2e`), and LLM quality (`llm`).

To run all tests:
```bash
pytest