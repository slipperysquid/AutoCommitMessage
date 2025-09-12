
import json
import csv
from langsmith import Client
from dotenv import load_dotenv, find_dotenv



load_dotenv(find_dotenv())

client = Client()

dataset_name = "git diff --staged outputs"


dl_dataset = client.create_dataset(
   dataset_name=dataset_name,
   description="A bunch of example git diff command outputs",
   )


with open('tests/langsmith/examples.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        # Now, 'row' is a dictionary like:
        # {'commit_type': 'feat', 'description': '...', 'diff_content': '...'}
        
        client.create_example(
            inputs={"input": row["diff_content"]}, # Access the column by its header name
            outputs=None,
            dataset_id='9a3ea93c-b7ca-4856-b808-8f6ad849eb31'#dl_dataset.id,
        )
        print(f"Example created for commit type: {row['commit_type']}")
        
        


