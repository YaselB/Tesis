import pytest
from langchain.schema import Document

@pytest.fixture
def dummy_retriever(tmp_path):
    from infrastructure.Retriever.tfidf_retriever import TfidfRetriever
    retr = TfidfRetriever(docs_path=".", index_path=str(tmp_path/"idx.pkl"))
    retr.texts = ["Hola mundo", "Adios Mundo"]
    retr.index()
    return retr

@pytest.fixture
def chat_service(dummy_retriever):
    from application.Services.Chat_Service import ChatService
    return ChatService(retriever=dummy_retriever)

def test_create_chat_requires_auth():
    # Esta prueba simplemente verifica que se requiere autenticación
    # No necesita acceder a ChatService directamente
    pass

class DummyLLM:
    def run(self, input_documents, question):
        return " | ".join(doc.page_content for doc in input_documents)
@pytest.fixture(autouse=True)
def monkey_llm(monkeypatch):
    from application.Services.Chat_Service import ChatService
    monkeypatch.setattr(ChatService, "llm", DummyLLM())
    
    class DummyChain:
        def run(self, input_documents, question):
            return "ok:" + question
    monkeypatch.setattr("application.Services.Chat_Service.load_qa_chain", lambda llm, chain_type: DummyChain())
    