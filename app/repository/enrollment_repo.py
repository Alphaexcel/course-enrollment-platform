from sqlalchemy.orm import Session 
from app.models.enrollment import Enrollment

def get_enrollment(db: Session, user_id: int, course_id: int):
    return db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()

def get_enrollment_by_id(db: Session, enrollment_id: int):
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

def get_all_enrollments(db: Session):
    return db.query(Enrollment).all()

def get_enrollment_by_course(db: Session, course_id: int):
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()

def get_enrollment_by_user(db: Session, user_id: int):
    return db.query(Enrollment).filter(Enrollment.user_id == user_id).all()

def count_enrollment_for_course(db: Session, course_id: int) -> int:
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).count()

def create_enrollment(db: Session, user_id: int, course_id: int):
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

def delete_enrollment(db: Session, enrollment: Enrollment):
    db.delete(enrollment)
    db.commit()