from locust import HttpUser, task, between
import random

class ChatUser(HttpUser):
    wait_time = between(1, 5)  # Simulate thinking time between 1-5 seconds

    @task(1)
    def warmup_greeting(self):
        """Simple greeting to warm up connection/cache."""
        self.client.post("/api/chat", json={"message": "Hei"})

    @task(3)
    def query_general(self):
        """General list query - hits RAG with broad search."""
        self.client.post("/api/chat", json={"message": "Hvilke årsstudium tilbys?"})

    @task(3)
    def query_specific(self):
        """Specific query - hits RAG with targeted search."""
        queries = [
            "Fortell om årsstudium i IT",
            "Hva lærer man på logistikk?",
            "Hvordan søker man opptak?",
            "Hvem er kontaktperson for Molde campus?"
        ]
        self.client.post("/api/chat", json={"message": random.choice(queries)})

    def on_start(self):
        """Called when a User starts running."""
        # Optional: Login logic if we wanted to test auth, but chat is public-ish or we assume token
        pass
