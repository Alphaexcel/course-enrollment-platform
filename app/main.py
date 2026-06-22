import os
from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.routers import auth, users, courses, enrollments

try: 
    Base.metadata.create_all(bind=engine)
    print('Database tables created successfully')
except Exception as e:
    print(f"Databse connection error: {e}")

app = FastAPI(
    title="Course Enrollment Platform",
    description="AltSchool Capstone - FastAPI backend for course enrollment",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)




@app.get("/", tags=["Health"])
def root():
    return {"message": "Course Enrollment Platform API is running"}

