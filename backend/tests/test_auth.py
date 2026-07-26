from app.core.security import verify_password


def test_login_success(client, test_staff):
    response = client.post(
        "/auth/login",
        json={"username": "testdoc", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure(client):
    response = client.post(
        "/auth/login",
        json={"username": "testdoc", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_me(client, test_staff, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["staff_id"] == str(test_staff.staff_id)
    assert data["first_name"] == "Test"


def test_change_password(client, test_staff, auth_headers, db):
    response = client.post(
        "/auth/change-password",
        headers=auth_headers,
        json={"old_password": "password123", "new_password": "newsecurepass"},
    )
    assert response.status_code == 200

    db.refresh(test_staff)
    cred = test_staff.credentials[0] if hasattr(test_staff, "credentials") else None
    if cred:
        assert verify_password("newsecurepass", cred.password_hash)