from langchain.chat_models import ChatOpenAI

class DeepSeekLLM(ChatOpenAI):
    """
    LLM usando OpenRouter para acceder al modelo gratuito de DeepSeek.
    """
    def __init__(
        self,
        api_key: str = None,
        model: str = "mistralai/mistral-small-3.1-24b-instruct:free",
        temperature: float = 0.0
    ):
        key = api_key or "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"
        super().__init__(
            openai_api_key=key,
            openai_api_base="https://openrouter.ai/api/v1",
            model=model,
            temperature=temperature
        )
