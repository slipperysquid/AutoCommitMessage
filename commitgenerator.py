import subprocess
from git import Repo

class CommitGenerator:
    
    def __init__(self):
        self.repo = Repo('.')
    
    def get_parsed_differences(self):
        
        differences = self.repo.index.diff("HEAD")
        
        for diff in differences:
            print(diff)
        
        
        


gen = CommitGenerator()

gen.get_parsed_differences()