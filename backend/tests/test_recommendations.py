from unittest.mock import patch


def test_recommendations_keyword_fallback(client):
    """Recommendations must work even without Groq (fallback mode)."""
    payload = {
        "query": "I have back pain",
        "city": "Lahore",
        "consultation_type": "online",
    }
    response = client.post("/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "detected_specialization" in data
    assert "recommended_doctors" in data
    assert "safety_note" in data


def test_recommendations_returns_orthopedic_for_back_pain(client):
    """Back pain should detect Orthopedic specialization via keyword fallback."""
    # Create an orthopedic doctor first
    client.post("/doctors", json={
        "name": "Dr. Ortho",
        "email": "ortho@example.com",
        "specialization": "Orthopedic",
        "city": "Lahore",
        "consultation_type": "online",
        "experience_years": 8,
        "rating": 4.8,
        "is_available": True,
    })

    payload = {"query": "I have back pain", "city": "Lahore"}
    response = client.post("/recommendations", json=payload)
    data = response.json()
    assert data["detected_specialization"] == "Orthopedic"


def test_recommendations_response_fields(client):
    payload = {"query": "skin allergy", "city": "Karachi"}
    response = client.post("/recommendations", json=payload)
    data = response.json()
    assert "detected_specialization" in data
    assert "recommended_doctors" in data
    assert isinstance(data["recommended_doctors"], list)
