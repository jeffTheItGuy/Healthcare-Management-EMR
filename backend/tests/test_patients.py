from app.models.patient import Patient


def test_create_patient(client, auth_headers):
    payload = {
        "patient_number": "P-2024-000001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "gender": "MALE",
        "phone_primary": "5550001",
    }
    response = client.post("/patients/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["patient_id"] is not None


def test_get_patient(client, auth_headers, db):
    patient = Patient(
        patient_number="P-2024-000002",
        first_name="Jane",
        last_name="Doe",
        date_of_birth="1995-05-15",
        gender="FEMALE",
        is_active=True,
    )
    db.add(patient)
    db.commit()

    response = client.get(f"/patients/{patient.patient_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"


def test_search_patients(client, auth_headers, db):
    for i in range(3):
        db.add(
            Patient(
                patient_number=f"P-2024-{100000+i}",
                first_name=f"Patient{i}",
                last_name="Test",
                date_of_birth="2000-01-01",
                gender="MALE",
                is_active=True,
            )
        )
    db.commit()

    response = client.get("/patients/?q=Patient1", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1