
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_http_rejected():
    # Simula llamada insegura
    r = client.get("http://127.0.0.1:8000/docs")
    assert r.status_code in (400, 426)  # Bad Request o Upgrade Required
