from app.database import SessionLocal, get_db
from fastapi import APIRouter, Depends
from app.middleware.auth import oauth2_scheme 
from app.crud.user import get_user_by_id, get_all_users, update_user, delete_user
from app.schemas.user import User

router = APIRouter()

@router.get("/users", dependencies=[Depends(oauth2_scheme)])
def get_users_handler(db: SessionLocal = Depends(get_db)):
	try:
		users = get_all_users(db)
		return users
	except Exception as e:
		return {"error": str(e)}

@router.get("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def get_user_by_id_handler(user_id: str, db: SessionLocal = Depends(get_db)):
	try:
		user = get_user_by_id(db, user_id)
		if user is None:
			return {"error": "User not found"}
		return User(**user.__dict__)
	except Exception as e:
		return {"error": str(e)}

@router.put("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
async def update_user_handler(user_id: str, user: User, db: SessionLocal = Depends(get_db)):
	try:
		return await update_user(db, user_id, user)
	except Exception as e:
		return {"error": str(e)}

@router.delete("/users/{user_id}", dependencies=[Depends(oauth2_scheme)])
def delete_user_handler(user_id: str, db: SessionLocal = Depends(get_db)):
	try:
		delete_user(db, user_id)
		return "ok"
	except Exception as e:
		return {"error": str(e)}
