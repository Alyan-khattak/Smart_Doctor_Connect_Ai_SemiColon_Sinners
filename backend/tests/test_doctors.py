def test_get_all_doctors_empty(client):
    response = client.get("/doctors")
    assert response.status_code == 200
    assert response.json() == []


def test_create_doctor(client):
    payload = {
        "name": "Dr. Sara Malik",
        "email": "sara@example.com",
        "specialization": "Orthopedic",
        "city": "Lahore",
        "location": "Johar Town",
        "consultation_type": "both",
        "experience_years": 8,
        "rating": 4.8,
        "is_available": True,
        "bio": "Bone specialist",
    }
    response = client.post("/doctors", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Dr. Sara Malik"
    assert data["specialization"] == "Orthopedic"
    assert "id" in data


def test_get_doctor_by_id(client):
    # First create
    payload = {
        "name": "Dr. Test",
        "email": "test@example.com",
        "specialization": "Cardiologist",
        "city": "Karachi",
        "consultation_type": "online",
        "experience_years": 5,
        "rating": 4.5,
        "is_available": True,
    }
    create_resp = client.post("/doctors", json=payload)
    doc_id = create_resp.json()["id"]

    response = client.get(f"/doctors/{doc_id}")
    assert response.status_code == 200
    assert response.json()["id"] == doc_id


def test_get_doctor_not_found(client):
    response = client.get("/doctors/9999")
    assert response.status_code == 404


def test_update_doctor(client):
    payload = {
        "name": "Dr. Update Test",
        "email": "update@example.com",
        "specialization": "Neurologist",
        "city": "Islamabad",
        "consultation_type": "physical",
        "experience_years": 3,
        "rating": 4.0,
        "is_available": True,
    }
    create_resp = client.post("/doctors", json=payload)
    doc_id = create_resp.json()["id"]

    update_resp = client.put(f"/doctors/{doc_id}", json={"is_available": False})
    assert update_resp.status_code == 200
    assert update_resp.json()["is_available"] is False


def test_search_doctors(client):
    payload = {
        "name": "Dr. Search Test",
        "email": "search@example.com",
        "specialization": "Dermatologist",
        "city": "Lahore",
        "consultation_type": "online",
        "experience_years": 4,
        "rating": 4.3,
        "is_available": True,
    }
    client.post("/doctors", json=payload)

    response = client.get("/doctors/search?city=Lahore")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) >= 1
