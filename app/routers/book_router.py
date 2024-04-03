from fastapi import APIRouter, Depends, Request
from app.database import SessionLocal, get_db
from app.schemas.book import BookBase, Book
from app.crud.book import create_book, get_all_books, get_book_by_id, update_book, delete_book, get_borrowed_books, borrow_book, return_book, delete_borrow
from app.middleware.auth import oauth2_scheme
from app.util.auth import check_user_role

router = APIRouter()


@router.post("/books", dependencies=[Depends(oauth2_scheme)])
def create_book_handler(request: Request, book: BookBase, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=2)
	return create_book(db, book)

@router.get("/books", dependencies=[Depends(oauth2_scheme)])
def get_all_books_handler(request: Request, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=2)
	books = get_all_books(db)
	return books

@router.get("/books/{book_id}", dependencies=[Depends(oauth2_scheme)])
def read_book_handler(book_id: str, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=2)
	book = get_book_by_id(db, book_id)
	if book is None:
		return {"error": "Book not found"}
	return book

@router.put("/books/{book_id}", dependencies=[Depends(oauth2_scheme)])
def update_book_handler(request: Request, book_id: str, book: Book, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=2)
	return update_book(db, book_id, book)

@router.delete("/books/{book_id}", dependencies=[Depends(oauth2_scheme)])
def delete_book_handler(request: Request, book_id: str, db: SessionLocal = Depends(get_db)):
	delete_book(db, book_id)
	return "ok"


@router.get("/borrowed/books", dependencies=[Depends(oauth2_scheme)])
def get_borrowed_books_handler(request: Request, user_id: str = None, isbn: str = None, book_id: str = None, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=1)
	return get_borrowed_books(db, user_id, isbn, book_id)
	
@router.post("/books/{book_id}/borrow/{user_id}", dependencies=[Depends(oauth2_scheme)])
def borrow_book_handler(request: Request, book_id: str, user_id: str, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=2)
	return borrow_book(db, user_id, book_id)

@router.put("/books/return/{borrow_id}", dependencies=[Depends(oauth2_scheme)])
def return_book_handler(request: Request, borrow_id: str, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=2)
	return return_book(db, borrow_id)

@router.delete("/borrow/{borrow_id}", dependencies=[Depends(oauth2_scheme)])
def delete_borrow_handler(request: Request, borrow_id: str, db: SessionLocal = Depends(get_db)):
	check_user_role(request, min_role=2)
	return delete_borrow(db, borrow_id)