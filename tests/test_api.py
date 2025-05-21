import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture()
def client():
    return TestClient(app)
def test_create_chat_requires_auth(client):
    r = client.post("/create_new_chat/1")
    assert r.status_code == 403 or r.status_code == 401

def test_ask_endpoint(client , monkeypatch):
    monkeypatch.setenv("DEMO" , "OK")
    import application.Services.Chat_Service as svcmod
    monkeypatch.setattr(svcmod.Chat_Service , "answer" , lambda self , q , idc: "resp")
    headers = {"Authorization" : "Bearer faketoken"}
    payload = {"question" , "hola" ,"id_chat" }
    r = client.post("/ask" , json= payload ,headers = headers)
    assert r.status_code == 200
    assert r.json() == {"response": "resp"}