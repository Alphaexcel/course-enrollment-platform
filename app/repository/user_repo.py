from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()




def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()




def create_user(db: Session, user: UserCreate):
    password_bytes = user.password.encode("utf-8")[:72]
    hashed = pwd_context.hash(password_bytes.decode("utf-8"))
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(password_bytes.decode("utf-8"), hashed_password)

