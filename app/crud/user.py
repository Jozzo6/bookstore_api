import uuid
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, User as UserSchema
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

def get_user_by_id(db: Session, user_id: str) -> User: 
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()
    
def get_user_by_email(db: Session, email: str) -> User:
	return db.query(User).filter(User.email == email).first()

async def update_user(db: Session, user_id: str, user: UserSchema) -> UserSchema:
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.email = user.email
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.type = user.type.value
        db.commit()
        db.refresh(db_user)
        return UserSchema(**db_user.__dict__)
    except Exception as e:
        db.rollback()
        raise ValueError("An error occurred while updating user: " + str(e))

def delete_user(db: Session, user_id: str):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        db.delete(db_user)
        db.commit()
        return db_user
    except Exception as e:
        db.rollback()
        raise ValueError("An error occurred while deleting user: " + str(e))

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user
