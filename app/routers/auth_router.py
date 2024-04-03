from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.crud.user import create_user, get_user_by_email, authenticate_user
from app.schemas.user import User, UserCreate
from app.database import get_db
from app.util.auth import create_access_token
from app.config import EnvironmentVariables

router = APIRouter()

class AuthResponse(BaseModel):
	access_token: str
	user: User

@router.post("/auth/login", response_model=AuthResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id), "user_type": user.type}
    )
    return AuthResponse(access_token=access_token, user=user)

@router.post("/auth/register", response_model=AuthResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
	try:
		db_user = get_user_by_email(db, email=user.email)
		if db_user:
			raise HTTPException(status_code=400, detail="Email already in use")
		user = create_user(db=db, user=user)
		access_token = create_access_token(data={"sub": user.email})
		return AuthResponse(access_token=access_token, user=user)
	except Exception as e:
		raise HTTPException(status_code=500, detail="An error occurred while creating user: " + str(e))
