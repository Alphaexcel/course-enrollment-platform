from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.user import UserOut
from app.schemas.course import CourseOut




class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)


    id: int
    user_id: int
    course_id: int
    created_at: datetime




class EnrollmentDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)


    id: int
    user_id: int
    course_id: int
    created_at: datetime
    user: UserOut
    course: CourseOut
