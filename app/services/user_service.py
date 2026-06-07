from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository import user_repo
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import create_access_token


def register_user(db: Session, user_data: UserCreate):
    existing = user_repo.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return user_repo.create_user(db, user_data)

def login_user(db: Session, login_data: UserLogin):
    user = user_repo.get_user_by_email(db, login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    if not user_repo.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}