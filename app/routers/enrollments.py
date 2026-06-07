from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.enrollment import EnrollmentOut
from app.services.enrollment_service import (
    enroll_student, deregister_student,
    get_all_enrollments, get_enrollments_for_course,
    admin_remove_student
)
from app.dependencies import get_current_student, get_current_admin
from app.models.user import User


router = APIRouter(prefix="/enrollments", tags=["Enrollments"])




# --- STATIC ROUTES FIRST ---


@router.get("/", response_model=List[EnrollmentOut])
def all_enrollments(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return get_all_enrollments(db)




@router.get("/course/{course_id}", response_model=List[EnrollmentOut])
def course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return get_enrollments_for_course(db, course_id)




@router.delete("/admin/{enrollment_id}")
def admin_remove(
    enrollment_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return admin_remove_student(db, enrollment_id)




# --- DYNAMIC ROUTES AFTER ---


@router.post("/{course_id}", response_model=EnrollmentOut, status_code=201)
def enroll(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    return enroll_student(db, current_user, course_id)




@router.delete("/{course_id}")
def deregister(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    return deregister_student(db, current_user, course_id)

