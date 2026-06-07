from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.course import CourseCreate, CourseUpdate, CourseOut
from app.services.course_service import (
    get_all_courses, get_course, create_course, update_course, delete_course
)
from app.dependencies import get_current_admin

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=List[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return get_all_courses(db)

@router.get("/{course_id}", response_model=CourseOut)
def retrieve_course(course_id: int, db: Session = Depends(get_db)):
    return get_course(db, course_id)

@router.post("/", response_model=CourseOut, status_code=201)
def add_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return create_course(db, course_data)

@router.patch("/{course_id}", response_model=CourseOut)
def modify_course(
    course_id: int,
    updates: CourseUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return update_course(db, course_id, updates)

@router.delete("/{course_id}")
def remove_course(
    course_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return delete_course(db, course_id)