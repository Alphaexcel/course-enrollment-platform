from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate

def get_all_active_courses(db: Session):
    return db.query(Course).filter(Course.is_active == True).all()

def get_course_by_id(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

def get_course_by_code(db: Session, code:str):
    return db.query(Course).filter(Course.code == code).first()

def create_course(db: Session, course: CourseCreate):
    db_course = Course(
        title=course.title,
        code=course.code,
        capacity= course.capacity,
    )
    db.add(db_course)
    db.commit()
    return db_course

def update_course(db: Session, course: Course, updates: CourseUpdate):
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

def delete_course(db: Session, course: Course):
    db.delete(course)
    db.commit()