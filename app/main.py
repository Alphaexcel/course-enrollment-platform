@"
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.routers import auth, users, courses, enrollments

try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Database connection error: {e}")

app = FastAPI(
    title="Course Enrollment Platform",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__}
    )

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Course Enrollment Platform API is running"}
"@ | Set-Content app\main.py
