from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository import enrollment_repo, course_repo
from app.models.user import User

def enroll_student(db: Session, current_user: User, course_id: int):
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not course.is_active:
        raise HTTPException(status_code=400, detail="Course is not active")
    
    existing = enrollment_repo.get_enrollment(db, current_user.id, course_id)
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    count = enrollment_repo.count_enrollment_for_course(db, course_id)
    if count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course is full")
    
    return enrollment_repo.create_enrollment(db, current_user.id, course_id)


def deregister_student(db: Session, current_user: User, course_id: int):
    enrollment = enrollment_repo.get_enrollment(db, current_user.id, course_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment_repo.delete_enrollment(db, enrollment)
    return {"detail": "Successfully deregistered from course"}

def get_all_enrollments(db: Session):
    return enrollment_repo.get_all_enrollments(db)

def get_enrollments_for_course(db: Session, course_id: int):
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return enrollment_repo.get_enrollment_by_course(db, course_id)

def admin_remove_student(db: Session, enrollment_id: int):
    enrollment = enrollment_repo.get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment_repo.delete_enrollment(db, enrollment)
    return {"detail": "Student removed from course"}