import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from main import app
from infrastructure.Retriever.tfidf_retriever import TfidfRetriever
from application.Services.Chat_Service import ChatService

pytest_plugins = ["pytest_asyncio"]
asyncio_fixture_loop_scope = "function"

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def dummy_retriever(tmp_path):
    retr = TfidfRetriever(docs_path=".", index_path=str(tmp_path/"idx.pkl"))
    retr.texts = ["Hola mundo", "Adios Mundo"]
    retr.index()
    return retr

@pytest.fixture
def chat_service(dummy_retriever):
    return ChatService(retriever=dummy_retriever)

def pytest_configure(config):
    config.addinivalue_line("markers", "benchmark: mark a test as a benchmark")