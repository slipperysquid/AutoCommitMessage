import pytest
from git import Repo
import os
from langchain_core.messages import AIMessage
from autocommitmessage.commit_generator import CommitGenerator
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

requires_api_key = pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="This test requires a GOOGLE_API_KEY in the environment"
)

@pytest.fixture
def test_repo(tmpdir):
    repo_path = tmpdir.strpath

    repo = Repo.init(repo_path)

    original_cwd = os.getcwd()
    os.chdir(repo_path)

    yield repo

    os.chdir(original_cwd)

@pytest.mark.e2e
@requires_api_key
def test_generate_commit_with_real_staged_changes(test_repo):
    
    file_path = os.path.join(test_repo.working_tree_dir, "new_feature.py")
    with open(file_path, "w") as f:
        f.write("def my_new_feature():\n    return True")
    
    test_repo.index.add([file_path])


    
    gen = CommitGenerator()
    commit_message = gen.generate()

    
    assert commit_message is not None
    assert len(commit_message) > 10 
    valid_types = ["feat", "fix", "chore", "refactor", "docs", "style", "test"]
    assert any(commit_message.startswith(t) for t in valid_types)

    diff_content = test_repo.git.diff('--staged')
    assert "+def my_new_feature()" in diff_content
    
    