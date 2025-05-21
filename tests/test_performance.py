
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
HEADERS = {"Authorization": "Bearer faketoken"}
PAYLOAD = {"question": "hola", "id_chat": 1}

@pytest.mark.benchmark(group="ask-endpoint")
def test_ask_latency(benchmark):
    def call():
        r = client.post("/ask", json=PAYLOAD, headers=HEADERS)
        assert r.status_code == 200
    # Benchmark: 5 iteraciones
    result = benchmark.pedantic(call, iterations=5, rounds=2)
    assert result.mean < 2.0
