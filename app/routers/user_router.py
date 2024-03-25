from fastapi import APIRouter, Depends
from app.middleware.auth import oauth2_scheme
from app.middleware.auth import jwt_auth_middleware

router = APIRouter()

@router.get("/users", dependencies=[Depends(oauth2_scheme)])
def read_users():
	return {"users": "users"}

@router.get("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def read_user(user_id: int):
	return {"user_id": user_id}

@router.put("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def update_user(user_id: int):
	return {"user_id": user_id}

@router.delete("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def delete_user(user_id: int):
	return {"user_id": user_id}
