
from locust import HttpUser, task, between

class ChatUser(HttpUser):
    wait_time = between(0, 1)
    @task(1)
    def ask(self):
        self.client.post("/ask", json={"question":"hola","id_chat":1}, headers={"Authorization":"Bearer faketoken"})
