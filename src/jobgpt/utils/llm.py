from langchain.callbacks import get_openai_callback
def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
    return {
        'result': result,
        'token_count': cb.total_tokens
    }