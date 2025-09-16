#Tests the LLMs generation quality using langsmith
import pytest
import os
from autocommitmessage.commit_generator import CommitGenerator
from langchain.smith import RunEvalConfig
from langchain.smith import run_on_dataset
from langsmith import Client
from autocommitmessage.llm import ChatGoogleGenerativeAIWithDelay
import uuid
from langchain.evaluation import load_evaluator
from langchain.evaluation.scoring.eval_chain import ScoreStringEvalChain


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
    
    evaluator_llm = ChatGoogleGenerativeAIWithDelay(
        model="gemini-2.5-flash", # Using a more powerful model for evaluation is often better
        temperature=0,
    )
    
    score_chain = ScoreStringEvalChain.from_llm(
    llm=evaluator_llm,
    criteria="helpfulness",
)

    eval_config = RunEvalConfig(
    # custom_evaluators accepts actual StringEvaluator/RunEvaluator instances
    custom_evaluators=[score_chain],
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
    print(results)
    for run_data in results['results'].values():
        # The score is inside the first item of the 'feedback' list.
        # The 'EvaluationResult' object has a .score attribute.
        score = run_data['feedback'][0].score
        run_id = run_data['run_id']

        # Based on your output, the scores are on a 1-10 scale (e.g., 9, 10).
        # Your assertion should reflect this scale.
        assert score >= 9, (
            f"Evaluation for run {run_id} failed. "
            f"Got score {score}, but expected at least 9."
        )
