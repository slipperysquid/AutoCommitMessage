import subprocess
from git import Repo
from llm import ChatGoogleGenerativeAIWithDelay
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from prompts import PROMPT
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
                print(f"Error while initializing repo: {e}")
                exit()
        
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
    load_dotenv(find_dotenv())
    gen = CommitGenerator()

    print(gen.generate())


if __name__ == '__main__':
    main()
    
