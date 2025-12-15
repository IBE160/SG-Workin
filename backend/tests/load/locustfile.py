from locust import HttpUser, task, between

class ChatUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def health_check(self):
        self.client.get("/api/health")

    @task(3)
    def chat_query(self):
        self.client.post("/api/chat", json={
            "message": "What are the admission requirements for nursing?",
            "history": []
        })
