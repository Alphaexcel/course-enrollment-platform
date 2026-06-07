def test_enroll_student(client, student_token, sample_course):
    course_id = sample_course["id"]
    response = client.post(f"/enrollments/{course_id}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    assert response.status_code == 201
    assert response.json()["course_id"] == course_id


def test_enroll_twice_fails(client, student_token, sample_course):
    course_id = sample_course["id"]
    # First enrollment
    client.post(f"/enrollments/{course_id}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    # Second enrollment
    response = client.post(f"/enrollments/{course_id}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    assert response.status_code == 400
    assert "Already enrolled" in response.json()["detail"]


def test_enroll_inactive_course_fails(client, student_token, sample_course, admin_token):
    course_id = sample_course["id"]
    # Deactivate the course
    client.patch(f"/courses/{course_id}", json={
        "is_active": False
    }, headers={"Authorization": f"Bearer {admin_token}"})
    # Attempt to enroll
    response = client.post(f"/enrollments/{course_id}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    assert response.status_code == 400
    assert "Course is not active" in response.json()["detail"]


def test_enroll_full_course_fails(client, admin_token, client_factory=None):
    # Create a course with capacity 1
    token_resp = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "adminpass"
    })
    # Register two students 
    client.post("/auth/register", json={
        "name": "S1", 
        "email": "s1@test.com",
        "password": "pass",
        "role": "student"
    })
    client.post("/auth/register", json={
        "name": "S2", 
        "email": "s2@test.com",
        "password": "pass",
        "role": "student"
    })
    course = client.post("/courses/", json={
        "title": "Tiny Course",
        "code": "TINY101",
        "capacity": 1
    }, headers={"Authorization": f"Bearer {admin_token}"}).json()

    t1 = client.post("/auth/login", json={
        "email": "s1@test.com",
        "password": "pass"
    }).json()["access_token"]
    t2 = client.post("/auth/login", json={
        "email": "s2@test.com",
        "password": "pass"
    }).json()["access_token"]

    client.post(f"/enrollments/{course['id']}", headers={"Authorization": f"Bearer {t1}"})
    response = client.post(f"/enrollments/{course['id']}", headers={"Authorization": f"Bearer {t2}"})
    assert response.status_code == 400
    assert "Course is full" in response.json()["detail"]


def test_admin_cannot_enroll(client, admin_token, sample_course):
    course_id = sample_course["id"]
    response = client.post(f"/enrollments/{course_id}", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert response.status_code == 403  


def test_deregister_student(client, student_token, sample_course):
    course_id = sample_course["id"]
    # Enroll first
    client.post(f"/enrollments/{course_id}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    response = client.delete(f"/enrollments/{course_id}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    assert response.status_code == 200


def test_admin_view_all_enrollments(client, admin_token, student_token, sample_course):
    course_id = sample_course["id"]
    client.post(f"/enrollments/{course_id}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    response = client.get("/enrollments/", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_student_cannot_view_all_enrollments(client, student_token):
    response = client.get("/enrollments/", headers={
        "Authorization": f"Bearer {student_token}"
    })
    assert response.status_code == 403


def test_admin_view_course_enrollments(client, admin_token, student_token, sample_course):
    course_id = sample_course["id"]
    client.post(f"/enrollments/{course_id}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    response = client.get(f"/enrollments/course/{course_id}", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert response.status_code == 200


def test_admin_remove_student(client, admin_token):
    # Create course
    course = client.post("/courses/", json={
        "title": "Remove Test Course",
        "code": "RMV101",
        "capacity": 10
    }, headers={"Authorization": f"Bearer {admin_token}"}).json()


    # Register and login a fresh student
    client.post("/auth/register", json={
        "name": "Remove Student",
        "email": "remove@test.com",
        "password": "removepass",
        "role": "student"
    })
    token_resp = client.post("/auth/login", json={
        "email": "remove@test.com",
        "password": "removepass"
    })
    student_token = token_resp.json()["access_token"]


    # Enroll the student
    enroll_response = client.post(f"/enrollments/{course['id']}", headers={
        "Authorization": f"Bearer {student_token}"
    })
    assert enroll_response.status_code == 201
    enrollment_id = enroll_response.json()["id"]


    # Admin removes the student
    response = client.delete(f"/enrollments/admin/{enrollment_id}", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert response.status_code == 200
