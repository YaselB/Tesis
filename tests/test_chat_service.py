import pytest
from langchain.schema import Document

class DummyLLM:
    def run(self, input_documents , question):
        return " | ".join(doc.page_content for doc in input_documents)
@pytest.fixture(autouse=True)
def monkey_llm(monkeypatch):
    from application.Services.Chat_Service import ChatService
    monkeypatch.setattr(ChatService, "llm" , DummyLLM())
    
    class DummyChain:
        def run(self , input_documents , question):
            return "ok:" + question
    monkeypatch.setattr("application.Services.Chat_Service.load_qa_chain" , lambda llm , chain_type: DummyChain())
def test_answer(chat_service):
    chat_service.retriever.texts = ["uno" , "dos"]
    chat_service.retriever.index()
    resp = chat_service.answer("pregunta" , id_chat=1)
    assert resp.startwith("ok:pregunta")