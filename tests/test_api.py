import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture()
def client():
    return TestClient(app)

def test_create_chat_requires_auth(client):
    r = client.post("/create_new_chat/1")
    assert r.status_code == 403 or r.status_code == 401

def test_ask_endpoint(client, monkeypatch):
    monkeypatch.setenv("DEMO", "OK")
    import application.Services.Chat_Service as svcmod
    
    # Mockear el método answer del ChatService
    monkeypatch.setattr(svcmod.ChatService, "answer", lambda self, q, idc: f"Respuesta a: {q}")
    
    headers = {"Authorization": "Bearer faketoken"}
    payload = {"question": "hola", "id_chat": 1}
    r = client.post("/ask", json=payload, headers=headers)
    assert r.status_code == 200
    assert r.json() == {"response": "Respuesta a: hola"}

# Añadir prueba para crear un chat
def test_create_chat(client, monkeypatch):
    import application.Services.Chat_Service as svcmod
    
    # Mockear el método create_new_chat del ChatService
    monkeypatch.setattr(svcmod.ChatService, "create_new_chat", lambda self, id_user: {"id_chat": 1, "id_user": id_user})
    
    headers = {"Authorization": "Bearer faketoken"}
    r = client.post("/create_new_chat/2", headers=headers)
    assert r.status_code == 200
    assert r.json() == {"id_chat": 1, "id_user": 2}
