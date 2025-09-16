import pytest
from unittest.mock import MagicMock
from autocommitmessage.commit_generator import CommitGenerator

FAKE_GIT_DIFF = """
diff --git a/main.py b/main.py
index e69de29..a3d4d2d 100644
--- a/main.py
+++ b/main.py
@@ -0,0 +1,5 @@
+def hello_world():
+    print("Hello, World!")
+
+if __name__ == "__main__":
+    hello_world()
"""

def test_get_difference():
    mock_repo = MagicMock()
    mock_repo.git.diff.return_value = FAKE_GIT_DIFF
    mock_llm = MagicMock()
    
    gen = CommitGenerator(repo=mock_repo,llm=mock_llm)
    differences = gen.get_differences()
    
    mock_repo.git.diff.assert_called_once_with("--staged")
    assert differences == FAKE_GIT_DIFF
    

def test_no_staged_changes():
    mock_repo = MagicMock()
    mock_repo.git.diff.return_value = ""
    mock_llm = MagicMock()

    gen = CommitGenerator(repo=mock_repo, llm=mock_llm)
    message = gen.generate()
    
    assert message == "No staged changes to commit."