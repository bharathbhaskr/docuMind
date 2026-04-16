from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "DocuMind" in response.json()["message"]

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_ask_without_document():
    response = client.post("/ask", json={
        "question": "test question",
        "document_id": "nonexistent_doc"
    })
    # Should return 200 with a "not found" answer, not crash
    assert response.status_code == 200