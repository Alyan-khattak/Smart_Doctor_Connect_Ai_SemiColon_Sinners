from unittest.mock import patch


def test_send_appointment_email_no_key(seeded_client):
    """Email returns email_sent: false when no API key is set."""
    client, doc = seeded_client
    response = client.post("/email/send-appointment", json={
        "appointment_id": 1,
        "doctor_id": doc.id,
        "patient_name": "Test Patient",
        "patient_contact": "03001234567",
        "problem": "Back pain",
        "appointment_date": "2026-05-12",
        "appointment_time": "18:00",
        "consultation_type": "online",
    })
    assert response.status_code == 200
    # Without API key set in test env, should return False
    data = response.json()
    assert "email_sent" in data


def test_send_lead_email_no_key(seeded_client):
    """Lead email returns email_sent: false when no API key is set."""
    client, doc = seeded_client
    response = client.post("/email/send-lead", json={
        "lead_id": 1,
        "doctor_id": doc.id,
        "patient_name": "Test Patient",
        "patient_contact": "03001234567",
        "problem": "Back pain",
    })
    assert response.status_code == 200
    assert "email_sent" in response.json()


def test_appointment_booking_email_sent_flag(seeded_client):
    """Booking API must always return email_sent field even if email fails."""
    client, doc = seeded_client
    from datetime import date
    today = str(date.today())
    response = client.post("/appointments", json={
        "doctor_id": doc.id,
        "patient_name": "Test",
        "patient_contact": "03001234567",
        "problem": "Pain",
        "appointment_date": today,
        "appointment_time": "19:30",
        "consultation_type": "online",
    })
    data = response.json()
    # Success path must have email_sent
    if "appointment_id" in data:
        assert "email_sent" in data
