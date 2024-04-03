from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import EnvironmentVariables
from fastapi import HTTPException, Request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    access_token_expires = timedelta(hours=int(EnvironmentVariables().ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": datetime.now() + access_token_expires})
    encoded_jwt = jwt.encode(to_encode, EnvironmentVariables().SECRET_KEY, algorithm=EnvironmentVariables().ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def check_user_role(request: Request, min_role: int):
    if request.state.user_type < min_role:
        print('User does not have the required role')
        raise HTTPException(status_code=403, detail="Forbidden")
    return