import subprocess
import os
from git import Repo
from .llm import ChatGoogleGenerativeAIWithDelay
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from .prompts import PROMPT
import json
from dotenv import load_dotenv, find_dotenv


class CommitGenerator:
    
    def __init__(self,repo=None,llm=None):
        
        if repo:
            self.repo = repo
        else:
            try:
                self.repo = Repo('.', search_parent_directories=True)
            except Exception as e:
                print(f"Error: Not a git repository. {e}")
                exit()
        
    
        dotenv_path = os.path.join(self.repo.working_tree_dir, '.env')
        load_dotenv(dotenv_path=dotenv_path)
        
        if llm:
            self.llm = llm
        else:
            
            self.llm = LLM = ChatGoogleGenerativeAIWithDelay(
                model="gemini-2.5-flash",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
            
        prompt = ChatPromptTemplate.from_template(PROMPT)
        self.generation_chain = prompt | self.llm | StrOutputParser()

    
    def get_differences(self):
        
        return self.repo.git.diff('--staged')
    
    def generate(self):
        
        all_diffs = self.get_differences()
        
        if not all_diffs:
            return "No staged changes to commit."
        
        invoke_parameters = {
            "input": all_diffs
        }

        commit_message = self.generation_chain.invoke(invoke_parameters)
        
        return commit_message
        
        

def main():
        
    gen = CommitGenerator()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found.")
        print("Please create a .env file in your repository's root directory and add your key:")
        print('GOOGLE_API_KEY="your_google_api_key_here"')
        exit()

    print("--- Generating Commit Message ---")
    print(gen.generate())


if __name__ == '__main__':
    main()
    
