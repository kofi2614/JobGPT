from langchain.callbacks import OpenAICallbackHandler
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
import os
from langchain.schema import AgentAction, AgentFinish, LLMResult
from typing import Any
import logging

class OpenAITokenandler(OpenAICallbackHandler):
    def __init__(self, model_name:str):
        super().__init__()
        self.model_name = model_name        

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:        
        token_usage = response.llm_output["token_usage"]
        total_tokens = token_usage["total_tokens"]
        prompt_tokens = token_usage["prompt_tokens"]
        completion_tokens = token_usage["completion_tokens"]                        
        log_metric = {
            "model_name": self.model_name,            
            "total_tokens": total_tokens,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,            
        }
        logging.info(log_metric)

def load_model(model_name="gpt-4", temperature=0.0):
    return ChatOpenAI(
            model_name=model_name,
            openai_api_key=os.environ["OPENAI_API_KEY"],
            temperature=temperature,
            verbose=True,
            callbacks=BaseCallbackManager([OpenAITokenandler(model_name=model_name)]),            
        )

def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
    return {
        'result': result,
        'token_count': cb.total_tokens
    }