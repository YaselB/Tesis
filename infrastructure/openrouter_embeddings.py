from langchain.embeddings.openai import OpenAIEmbeddings

def get_openrouter_embeddings(api_key: str , api_base: str):
    return OpenAIEmbeddings(
        model = "text-embedding-ada-002",
        openai_api_key = api_key,
        openai_api_base = api_base
    )
