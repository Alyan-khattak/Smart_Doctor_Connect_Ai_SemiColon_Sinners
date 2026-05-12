from datetime import date


def test_get_availability(seeded_client):
    client, doc = seeded_client
    today = str(date.today())
    response = client.get(f"/availability/{doc.id}?date={today}")
    assert response.status_code == 200
    data = response.json()
    assert data["doctor_id"] == doc.id
    assert "slots" in data
    assert len(data["slots"]) > 0
    assert "earliest_available_slot" in data


def test_add_slot(seeded_client):
    client, doc = seeded_client
    response = client.post(
        f"/availability/{doc.id}",
        json={"slot_date": "2030-01-01", "slot_time": "09:00"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["slot_time"] == "09:00"


def test_update_slot(seeded_client):
    client, doc = seeded_client
    today = str(date.today())
    avail = client.get(f"/availability/{doc.id}?date={today}").json()
    slot_id = avail["slots"][0]["slot_id"]

    response = client.put(f"/availability/slot/{slot_id}", json={"is_booked": True})
    assert response.status_code == 200
    assert response.json()["is_booked"] is True


def test_earliest_available_slot(seeded_client):
    client, doc = seeded_client
    today = str(date.today())
    data = client.get(f"/availability/{doc.id}?date={today}").json()
    assert data["earliest_available_slot"] is not None
