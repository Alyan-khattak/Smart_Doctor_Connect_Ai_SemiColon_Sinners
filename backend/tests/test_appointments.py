from datetime import date


def _book(client, doc_id, time="18:00"):
    today = str(date.today())
    return client.post("/appointments", json={
        "doctor_id": doc_id,
        "patient_name": "Ali Khan",
        "patient_contact": "03001234567",
        "problem": "Back pain",
        "appointment_date": today,
        "appointment_time": time,
        "consultation_type": "online",
    })


def test_book_appointment_success(seeded_client):
    client, doc = seeded_client
    response = _book(client, doc.id)
    assert response.status_code == 200
    data = response.json()
    assert "appointment_id" in data
    assert data["status"] == "pending"
    assert "email_sent" in data


def test_book_appointment_conflict(seeded_client):
    client, doc = seeded_client
    # Book once
    _book(client, doc.id, "17:00")
    # Book again same slot
    response = _book(client, doc.id, "17:00")
    assert response.status_code == 200
    data = response.json()
    assert "available_alternative_slots" in data
    assert "already booked" in data["message"].lower()


def test_get_appointment_by_id(seeded_client):
    client, doc = seeded_client
    book_resp = _book(client, doc.id).json()
    appt_id = book_resp["appointment_id"]

    response = client.get(f"/appointments/{appt_id}")
    assert response.status_code == 200
    assert response.json()["id"] == appt_id


def test_get_doctor_appointments(seeded_client):
    client, doc = seeded_client
    _book(client, doc.id)
    response = client.get(f"/appointments/doctor/{doc.id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_appointment_status(seeded_client):
    client, doc = seeded_client
    appt_id = _book(client, doc.id).json()["appointment_id"]
    response = client.put(f"/appointments/{appt_id}/status", json={"status": "confirmed"})
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"


def test_appointment_doctor_not_found(client):
    response = client.post("/appointments", json={
        "doctor_id": 9999,
        "patient_name": "Test",
        "patient_contact": "03001234567",
        "problem": "Test",
        "appointment_date": "2026-05-12",
        "appointment_time": "18:00",
        "consultation_type": "online",
    })
    assert response.status_code == 404
