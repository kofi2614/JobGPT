from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
import os

def load_model(model_name="gpt-4"):
    return ChatOpenAI(
            model_name=model_name,
            openai_api_key=os.environ["OPENAI_API_KEY"],
            temperature=0,
            verbose=True,
        )

def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
    return {
        'result': result,
        'token_count': cb.total_tokens
    }