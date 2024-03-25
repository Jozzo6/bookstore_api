from fastapi import APIRouter
from app.middleware.auth import jwt_auth_middleware

router = APIRouter()

@router.get("/books")
def read_books():
	return {"books": "books"}

@router.get("/books/{book_id}")
def read_book(book_id: int):
	return {"book_id": book_id}

@router.post("/books")
def create_book():
	return {"book": "book"}

@router.put("/books/{book_id}")
def update_book(book_id: int):
	return {"book_id": book_id}

@router.delete("/books/{book_id}")
def delete_book(book_id: int):
	return {"book_id": book_id}

@router.post("/books/{book_id}/users/{user_id}")
def add_user_to_book(book_id: int, user_id: int):
	return {"book_id": book_id, "user_id": user_id}

@router.put("/books-users/{id}")
def update_book_user(id: int):
	return {"id": id}

@router.delete("/books-users/{id}")
def delete_book_user(id: int):
	return {"id": id}