from app.database import SessionLocal, get_db
from fastapi import APIRouter, Depends, Request
from app.middleware.auth import oauth2_scheme 
from app.crud.user import get_user_by_id, get_all_users, update_user, delete_user
from app.schemas.user import User
from app.util.auth import check_user_role

router = APIRouter()

@router.get("/users", dependencies=[Depends(oauth2_scheme)])
def get_users_handler(request: Request, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=2)
	users = get_all_users(db)
	return users

@router.get("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def get_user_by_id_handler(request: Request, user_id: str, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=2)
	user = get_user_by_id(db, user_id)
	if user is None:
		return {"error": "User not found"}
	return User(**user.__dict__)

@router.put("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
async def update_user_handler(request: Request ,user_id: str, user: User, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=3)	
	return update_user(db, user_id, user)

@router.delete("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def delete_user_handler(request: Request, user_id: str, db: SessionLocal = Depends(get_db)):
	delete_user(db, user_id)
	return "ok"
