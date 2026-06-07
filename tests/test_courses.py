def test_list_courses_public(client, sample_course):
    response = client.get("/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_course_by_id(client, sample_course):
    course_id = sample_course["id"]
    response = client.get(f"/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["code"] == "PY101"


def test_get_nonexistent_course(client):
    response = client.get("/courses/999")
    assert response.status_code == 404


def test_create_course_as_admin(client, admin_token):
    response = client.post("/courses/", json={
        "title": "Django Advanced",
        "code": "DJ301",
        "capacity": 20
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    assert response.json()["code"] == "DJ301"


def test_create_course_duplicate_code(client, admin_token, sample_course):
    response = client.post("/courses/", json={
        "title": "Another Python",
        "code": "PY101",
        "capacity": 10
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 400


def test_create_course_invalid_capacity(client, admin_token):
    response = client.post("/courses/", json={
        "title": "Bad Course",
        "code": "BAD001",
        "capacity": 0
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 422


def test_create_course_as_student_fails(client, student_token):
    response = client.post("/courses/", json={
        "title": "Hack Course",
        "code": "Hack",
        "capacity": 5
    }, headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 403


def test_update_course(client, admin_token, sample_course):
    course_id = sample_course["id"]
    response = client.patch(f"/courses/{course_id}", json={
        "title": "Python Fundamentals",
        "is_active": False
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Python Fundamentals"
    assert response.json()["is_active"] == False


def test_delete_course(client, admin_token, sample_course):
    course_id = sample_course["id"]
    response = client.delete(f"/courses/{course_id}", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert response.status_code == 200


def test_delete_course_as_student_fails(client, student_token, sample_course):
    course_id = sample_course["id"]
    response = client.delete(f"/courses/{course_id}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    assert response.status_code == 403