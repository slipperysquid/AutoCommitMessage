
import time
from langchain_google_genai import ChatGoogleGenerativeAI # Correct import for Google GenAI
from langchain.chains import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import Any, List, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult



class ChatGoogleGenerativeAIWithDelay(ChatGoogleGenerativeAI):
    delay_seconds: float = 10.0

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        print(f"\n--- Waiting for {self.delay_seconds} second(s) before Google GenAI call ---")
        time.sleep(self.delay_seconds)

        print("--- Proceeding with Google GenAI call ---")
        return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)


