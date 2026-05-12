def test_chatbot_start_state(seeded_client):
    client, doc = seeded_client
    response = client.post("/chatbot/message", json={
        "doctor_id": doc.id,
        "message": "I want to contact the doctor",
        "conversation_state": "START",
        "collected_data": {
            "patient_name": None,
            "patient_contact": None,
            "problem": None,
        },
    })
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "next_state" in data
    assert "collected_data" in data
    assert "is_complete" in data


def test_chatbot_emergency_response(seeded_client):
    client, doc = seeded_client
    response = client.post("/chatbot/message", json={
        "doctor_id": doc.id,
        "message": "I am having a heart attack",
        "conversation_state": "START",
        "collected_data": {
            "patient_name": None,
            "patient_contact": None,
            "problem": None,
        },
    })
    data = response.json()
    assert "emergency" in data["reply"].lower() or "emergency" in data["next_state"].lower()


def test_save_lead(seeded_client):
    client, doc = seeded_client
    response = client.post("/chatbot/lead", json={
        "doctor_id": doc.id,
        "patient_name": "Ali Khan",
        "patient_contact": "03001234567",
        "problem": "Back pain",
    })
    assert response.status_code == 200
    data = response.json()
    assert "lead_id" in data
    assert "email_sent" in data
    assert "saved" in data["message"].lower() or "notified" in data["message"].lower()


def test_get_leads(seeded_client):
    client, doc = seeded_client
    # Save a lead first
    client.post("/chatbot/lead", json={
        "doctor_id": doc.id,
        "patient_name": "Test Patient",
        "patient_contact": "03009876543",
        "problem": "Knee pain",
    })
    response = client.get(f"/chatbot/leads/{doc.id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1
