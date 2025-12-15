from fastapi.testclient import TestClient
from main import app
from routers.messages import router

from core.constants import WELCOME_MESSAGE

client = TestClient(app)

def test_send_message():
    response = client.post(
        "/api/messages",
        json={"message": "Hello"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "success"
    assert json_response["data"]["response"] == WELCOME_MESSAGE
