import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    """Test that the health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_clarify_intent(client):
    """Test that the chat endpoint asks clarifying questions for vague input."""
    payload = {
        "messages": [
            {"role": "user", "content": "I need a test"}
        ]
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "reply" in data
    assert "recommendations" in data
    assert data["recommendations"] == []
    assert data["end_of_conversation"] is False

def test_chat_recommend_intent(client):
    """Test that the chat endpoint recommends assessments for specific input."""
    payload = {
        "messages": [
            {"role": "user", "content": "I am looking for a cognitive ability and numerical reasoning test for a software engineer"}
        ]
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "reply" in data
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    assert "name" in data["recommendations"][0]
    assert data["end_of_conversation"] is False

def test_chat_end_intent(client):
    """Test that the chat endpoint detects end of conversation."""
    payload = {
        "messages": [
            {"role": "user", "content": "thanks, goodbye"}
        ]
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["end_of_conversation"] is True
    assert "welcome" in data["reply"].lower() or "good luck" in data["reply"].lower()


def test_chat_details_intent(client):
    """Test that the chat endpoint returns details for a specific assessment."""
    payload = {
        "messages": [
            {"role": "user", "content": "pyTorch knowledge Test i want everything of this test"}
        ]
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "PyTorch Knowledge Test" in data["reply"]
    assert "Description" in data["reply"]
    assert len(data["recommendations"]) == 1
    assert data["recommendations"][0]["name"] == "PyTorch Knowledge Test"


def test_chat_add_intent(client):
    """Test that the chat endpoint allows adding new tests to the existing shortlist."""
    payload = {
        "messages": [
            {"role": "user", "content": "I want PyTorch Knowledge Test"},
            {"role": "assistant", "content": "Here is the list:\n\n| # | Name | Test Type | Keys | Duration | Languages | URL |\n|---|---|---|---|---|---|---|\n| 1 | PyTorch Knowledge Test | K | Knowledge & Skills | 15 minutes | English (USA) | <https://www.shl.com/products/product-catalog/view/smart-interview-live-coding/> |"},
            {"role": "user", "content": "now, I want also add aptitude test"}
        ]
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    recs = [r["name"] for r in data["recommendations"]]
    assert "PyTorch Knowledge Test" in recs
    assert any("Verify" in name or "Ability" in name or "Reasoning" in name or "Aptitude" in name for name in recs)


