from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional




class CourseCreate(BaseModel):
    title: str
    code: str
    capacity: int


    @field_validator("capacity")
    @classmethod
    def capacity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Capacity must be greater than zero")
        return v




class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None


    @field_validator("capacity")
    @classmethod
    def capacity_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Capacity must be greater than zero")
        return v




class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)


    id: int
    title: str
    code: str
    capacity: int
    is_active: bool
