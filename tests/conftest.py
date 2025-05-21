import pytest
from fastapi.testclient import TestClient
from main import app
from infrastructure.Retriever.tfidf_retriever import TfidfRetriever
from application.Services.Chat_Service import ChatService

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def dummy_retriever(tmp_path):
    retr = TfidRetriever(docs_path="." , index_path= str(tmp_path/"idx.pkl"))
    retr.texts = ["Hola mundo" , "Adios Mundo"]
    retr.index()
    return retr
@pytest.fixture()
def chat_service(dummy_retriever):
    return ChatService(retriever= dummy_retriever)
