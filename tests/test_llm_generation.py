#Tests the LLMs generation quality using langsmith
import pytest
import os
from commit_generator import CommitGenerator
from langchain.smith import RunEvalConfig
from langchain.smith import run_on_dataset
from langsmith import Client
from llm import ChatGoogleGenerativeAIWithDelay
import uuid

requires_google_api = pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="This test requires a GOOGLE_API_KEY in the environment"
)

requires_langsmith_api = pytest.mark.skipif(
    not os.getenv("LANGCHAIN_API_KEY"),
    reason="This test requires LANGCHAIN_API_KEY in the environment, make sure you get that and run all the langsmith ini programs"
    
)

@pytest.mark.llm
@requires_langsmith_api
@requires_google_api
def test_llm_generation_quality():
    project_name = f"quality-test-{uuid.uuid4().hex[:8]}"
    
    eval_config = RunEvalConfig(
        eval_llm = ChatGoogleGenerativeAIWithDelay(
            model="gemini-2.5-flash-lite",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,),
        evaluators=[
        RunEvalConfig.Criteria("conciseness"),
        RunEvalConfig.Criteria("coherence"),
        RunEvalConfig.Criteria("relevance"),
        RunEvalConfig.Criteria("helpfulness")
    ]
        )
    client = Client()
    gen = CommitGenerator()

    results = run_on_dataset(
    client=client,
    dataset_name="git diff --staged outputs",
    llm_or_chain_factory=gen.generation_chain,
    concurrency_level = 1,
    project_name=project_name,
    evaluation=eval_config
    )
    
    for r in results:
        for e in r["eval_results"]:
            assert e["score"] > 0.9, (
            f"'{e['evaluator']}' score failed. "
            f"Got {e['score']:.2f}, but expected at least {0.9:.2f}."
        )