def test_get_profile(client):
    # Register fresh user
    client.post("/auth/register", json={
        "name": "Profile User",
        "email": "profile@test.com",
        "password": "profilepass",
        "role": "student"
    })
    # Login to get token
    login = client.post("/auth/login", json={
        "email": "profile@test.com",
        "password": "profilepass"
    })
    assert login.status_code == 200
    token = login.json()["access_token"]


    # Get profile
    response = client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "profile@test.com"
    assert response.json()["role"] == "student"




def test_get_profile_unauthenticated(client):
    response = client.get("/users/me")
    assert response.status_code == 401




def test_get_profile_invalid_token(client):
    response = client.get("/users/me", headers={
        "Authorization": "Bearer invalidtoken"
    })
    assert response.status_code == 401
