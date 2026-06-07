# Course Enrollment Platform API 

A secure, database-backend RESTful API built with FastAPI for managing course enrollments.

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)
- JWT Authetication
- Pytest


## Setup Instructions

### 1 Clone the repository 
git clone <https://github.com/Alphaexcel/course-enrollment-platform>
cd course enrollment

## 2. Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate


### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure environment
Copy .env.example to .env and update values:
DATABASE_URL=postgresql://postgres:password@localhost:5432/enrollment_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

### 5. Create the database
createdb enrollment_db # or create vis psql

## Running Migrations
alembic upgrade head

## Running the Application
uvicorn app.main:app --reload

API docs available at: http://localhost:8000/docs

## Runing Tests
pytest test/ -v

Trst use SQLite in-memory database - no POstgreSQL neede for testing

## API Endpoints Summary

### Auth
POST /auth/register - Register a user
POST /auth/login - Login and get JWT token

### Users
GET /users/me - Get current user profile (autheticated)

### Courses
GET /courses/        - List all active courses (public)
GET /courses/{id}    - Get course by ID (public)
POST /courses/       - Create course (admin)
PATCH /courses/{id}  - Update course (admin)
DELETE /courses/{id} - Delete course (admin)


### Enollmentd 
POST   /enrollments/{course_id}      - Enroll in course (student)
DELETE /enrollments/{course_id}      - Deregister from course (student)
GET    /enrollments/                 - View all enrollments (admin)
GET    /enrollments/course/{course_id} -View course enrollments (admin)
DELETE /enrollments/admin/{id}      -Remove student from course (admin)


## Role-Based Access
- Students: view courses, enroll, deregister
- Admins: manage courses, view/manage all enrollments