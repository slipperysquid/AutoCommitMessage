import subprocess
from git import Repo
from llm import ChatGoogleGenerativeAIWithDelay
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from prompts import PROMPT
import json
from dotenv import load_dotenv, find_dotenv


class CommitGenerator:
    
    def __init__(self):
        try:
            self.repo = Repo('.', search_parent_directories=True)
        except Exception as e:
            print(f"Error while initializing repo: {e}")
            exit()
            
        self.llm = LLM = ChatGoogleGenerativeAIWithDelay(
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    
    def get_differences(self):
        
        return subprocess.run(["git","diff","--staged"], capture_output=True, text=True).stdout
    
    def generate(self):
        
        prompt = ChatPromptTemplate.from_template(PROMPT)
        
        all_diffs = self.get_differences()
        
        invoke_parameters = {
            "information": all_diffs
        }

        
        print(invoke_parameters["information"])
        generation_chain = prompt | self.llm | StrOutputParser()
        
        commit_message = generation_chain.invoke(invoke_parameters)
        
        return commit_message
        
        




if __name__ == '__main__':
    load_dotenv(find_dotenv())
    gen = CommitGenerator()

    print(gen.generate())
    
