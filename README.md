# AutoCommitMessage

AutoCommitMessage is a command-line tool that uses the power of Large Language Models (LLMs) to automatically generate descriptive and well-formatted git commit messages based on your staged changes.

## Features

* **AI-Powered Commits:** Leverages Google's Gemini models via LangChain to analyze your code differences and generate meaningful commit messages.
* **Free to Use:** This tool includes a wrapper around the Google API to ensure that your usage stays within the free tier, so you can use it without charge with your own Google API key.
* **Conventional Commits:** Follows the Conventional Commits specification to produce a clean and readable commit history. The generated messages include a type (e.g., `feat`, `fix`, `refactor`), an optional scope, and a concise description.
* **Seamless Git Integration:** Integrates directly with your local Git repository to automatically detect staged files.
* **Extensible and Testable:** Built with a modular structure, making it easy to test and extend. The project includes unit, end-to-end, and LLM quality tests.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd autocommitmessage
    ```

2.  **Install dependencies:**
    The project uses `setuptools` for packaging. You can install the necessary dependencies using pip. It's recommended to do this in a virtual environment.
    ```bash
    pip install .
    ```
    For development and running tests, install the testing dependencies:
    ```bash
    pip install .[dev]
    ```

3.  **Set up your environment:**
    You will need a Google API key to use the LLM. Create a `.env` file in the root of the project and add your key. For basic usage, you only need to provide the `GOOGLE_API_KEY`.

    ```
    GOOGLE_API_KEY="your_google_api_key_here"
    ```

    If you are running the development build to run tests, you will need to set up Langsmith for LLM quality testing.
    ```
    GOOGLE_API_KEY="your_google_api_key_here"
    LANGCHAIN_API_KEY="your_langchain_api_key"
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
    LANGCHAIN_PROJECT="your_project_name"
    ```
    You can get the `LANGCHAIN_PROJECT` name by running the `langsmith_ini.py` script:
    ```bash
    python tests/langsmith/langsmith_ini.py
    ```

## Usage

Once installed, you can run the tool from the command line within your git repository.

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

## Testing

This project uses `pytest` for testing. The tests are organized into three categories: unit, end-to-end (`e2e`), and LLM quality (`llm`).

To run all tests:
```bash
pytest