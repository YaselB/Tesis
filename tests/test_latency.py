from tokenize import group
import pytest

@pytest.mark.benchmark(group= " simple_query")
def test_ask_latency(client , benchmark):
    headers = {"Authorization": "Bearer faketoken"}
    payload = {"question": "hola" , "id_chat": 1}
    def call():
        client.post("/ask" , json= payload , headers = headers)
    result = benchmark.pedantic(call , iterations = 5 , rounds = 3)
    assert result.mean < 2.0