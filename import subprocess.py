import subprocess

class CommitGenerator:
    
    
    def generate():
        
        result = subprocess.run(['git','diff','--staged'], capture_output=True, text=True)
        