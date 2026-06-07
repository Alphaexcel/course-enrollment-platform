from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from typing import Optional




class UserRole(str, Enum):
    student = "student"
    admin = "admin"




class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.student




class UserLogin(BaseModel):
    email: EmailStr
    password: str




class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)


    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool




class Token(BaseModel):
    access_token: str
    token_type: str




class TokenData(BaseModel):
    email: Optional[str] = None
