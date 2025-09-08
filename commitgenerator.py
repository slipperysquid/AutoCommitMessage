import subprocess
from git import Repo

class CommitGenerator:
    
    def __init__(self):
        self.repo = Repo('.')
    
    def get_parsed_differences(self):
        
        differences = self.repo.index.diff(self.repo.head.commit, create_patch=True)
        
        for diff in differences:
            print(f"File: {diff.a_path if diff.a_path else diff.b_path}")
            print(f"Change type: {diff.change_type}") # e.g., 'A' for added, 'M' for modified, 'D' for deleted
            # You can also access the raw diff content if needed:
            #print(diff.b_blob.data_stream.read().decode('utf-8'))
            print(diff.diff.decode('utf-8'))
        
        
        




if __name__ == '__main__':

    gen = CommitGenerator()

    gen.get_parsed_differences()