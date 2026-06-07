def test_register_user(client):
    response = client.post("/auth/register", json={
        "name": "John Doe",
        "email": "john@test.com",
        "password": "secret123",
        "role": "student"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john@test.com"
    assert data["role"] == "student"




def test_register_duplicate_email(client):
    payload = {
        "name": "John Doe",
        "email": "john@test.com",
        "password": "secret123",
        "role": "student"
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]




def test_login_success(client):
    client.post("/auth/register", json={
        "name": "Jane",
        "email": "jane@test.com",
        "password": "pass123",
        "role": "student"
    })
    response = client.post("/auth/login", json={
        "email": "jane@test.com",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()




def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "name": "Jane",
        "email": "jane@test.com",
        "password": "pass123",
        "role": "student"
    })
    response = client.post("/auth/login", json={
        "email": "jane@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401




def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={
        "email": "ghost@test.com",
        "password": "pass"
    })
    assert response.status_code == 401




def test_register_invalid_role(client):
    response = client.post("/auth/register", json={
        "name": "Bad Role",
        "email": "bad@test.com",
        "password": "pass123",
        "role": "superuser"
    })
    assert response.status_code == 422
