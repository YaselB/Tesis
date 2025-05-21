import pytest
from fastapi.testclient import TestClient
from main import app

# Mantenemos solo la definición del fixture pero no las pruebas
@pytest.fixture
def setup_app_state(monkeypatch):
    from infrastructure.Retriever.tfidf_retriever import TfidfRetriever
    from application.Services.Chat_Service import ChatService
    
    # Configurar un retriever de prueba
    retriever = TfidfRetriever(docs_path=".")
    retriever.texts = ["Este es un documento de prueba", "Otro documento de prueba"]
    retriever.index()
    
    # Crear el servicio
    chat_service = ChatService(retriever=retriever)
    
    # Configurar app.state
    app.state.tfidf_retriever = retriever
    app.state.chat_service = chat_service
    
    return app

@pytest.fixture
def integration_client(setup_app_state):
    return TestClient(setup_app_state)