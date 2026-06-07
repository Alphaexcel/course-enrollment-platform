import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment


SQLALCHEMY_TEST_URL = "sqlite:///./test.db"


engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()




app.dependency_overrides[get_db] = override_get_db




@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)




@pytest.fixture
def client():
    return TestClient(app)




@pytest.fixture
def admin_token(client):
    reg = client.post("/auth/register", json={
        "name": "Admin User",
        "email": "admin@test.com",
        "password": "adminpass",
        "role": "admin"
    })
    assert reg.status_code == 201, f"Admin register failed: {reg.json()}"


    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "adminpass"
    })
    assert response.status_code == 200, f"Admin login failed: {response.json()}"
    return response.json()["access_token"]




@pytest.fixture
def student_token(client):
    reg = client.post("/auth/register", json={
        "name": "Student User",
        "email": "student@test.com",
        "password": "studentpass",
        "role": "student"
    })
    assert reg.status_code == 201, f"Student register failed: {reg.json()}"


    response = client.post("/auth/login", json={
        "email": "student@test.com",
        "password": "studentpass"
    })
    assert response.status_code == 200, f"Student login failed: {response.json()}"
    return response.json()["access_token"]




@pytest.fixture
def sample_course(client, admin_token):
    response = client.post("/courses/", json={
        "title": "Python Basics",
        "code": "PY101",
        "capacity": 5
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201, f"Course creation failed: {response.json()}"
    return response.json()

