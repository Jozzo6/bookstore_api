from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.util.auth import get_password_hash, verify_password


def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, first_name=user.first_name, last_name=user.last_name, type=user.type.value, password_hash=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise ValueError("An error occurred while creating user: " + str(e))
    
def get_user_by_email(db: Session, email: str) -> User:
	return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    print(user)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user
