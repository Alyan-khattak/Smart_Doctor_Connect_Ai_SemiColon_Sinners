from datetime import date


def test_dashboard_doctor_not_found(client):
    response = client.get("/dashboard/doctor/9999")
    assert response.status_code == 404


def test_dashboard_returns_all_fields(seeded_client):
    client, doc = seeded_client
    response = client.get(f"/dashboard/doctor/{doc.id}")
    assert response.status_code == 200
    data = response.json()
    assert "doctor" in data
    assert "stats" in data
    assert "appointments" in data
    assert "chatbot_leads" in data


def test_dashboard_stats_structure(seeded_client):
    client, doc = seeded_client
    data = client.get(f"/dashboard/doctor/{doc.id}").json()
    stats = data["stats"]
    assert "total_appointments" in stats
    assert "pending_appointments" in stats
    assert "today_appointments" in stats
    assert "new_chatbot_leads" in stats


def test_dashboard_shows_appointment(seeded_client):
    client, doc = seeded_client
    today = str(date.today())
    # Book an appointment
    client.post("/appointments", json={
        "doctor_id": doc.id,
        "patient_name": "Dashboard Test",
        "patient_contact": "03001234567",
        "problem": "Test",
        "appointment_date": today,
        "appointment_time": "17:00",
        "consultation_type": "online",
    })
    data = client.get(f"/dashboard/doctor/{doc.id}").json()
    assert data["stats"]["total_appointments"] >= 1


def test_dashboard_shows_lead(seeded_client):
    client, doc = seeded_client
    # Save a lead
    client.post("/chatbot/lead", json={
        "doctor_id": doc.id,
        "patient_name": "Lead Test",
        "patient_contact": "03009999999",
        "problem": "Neck pain",
    })
    data = client.get(f"/dashboard/doctor/{doc.id}").json()
    assert data["stats"]["new_chatbot_leads"] >= 1
    assert len(data["chatbot_leads"]) >= 1
