from sqlalchemy.orm import Session 
from fastapi import HTTPException, status
from app.repository import course_repo
from app.schemas.course import CourseCreate, CourseUpdate

def get_all_courses(db: Session):
    return course_repo.get_all_active_courses(db)

def get_course(db: Session, course_id: int):
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

def create_course(db: Session, course_data: CourseCreate):
    existing = course_repo.get_course_by_code(db, course_data.code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exixts"
        )
    return course_repo.create_course(db, course_data)

def update_course(db: Session, course_id: int, updates:CourseUpdate):
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if updates.code:
        existing = course_repo.get_course_by_code(db, updates.code)
        if existing and existing.id != course_id:
            raise HTTPException(status_code=400, detail="Course code already in use")
    return course_repo.update_course(db, course, updates)

def delete_course(db: Session, course_id: int):
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail= "Course not found")
    course_repo.delete_course(db, course)
    return {"detail": "Course deleted sucessfully"}