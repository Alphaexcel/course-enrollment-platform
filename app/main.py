from fastapi import FastAPI
from app.routers import auth, users, courses, enrollments


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

