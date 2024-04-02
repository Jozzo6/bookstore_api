from fastapi import APIRouter, Depends
from app.database import SessionLocal, get_db
from app.schemas.book import BookBase, Book
from app.crud.book import create_book, get_all_books, get_book_by_id, update_book, delete_book, get_borrowed_books, borrow_book, return_book

router = APIRouter()

@router.post("/books")
def create_book_handler(book: BookBase, db: SessionLocal = Depends(get_db)):
	try:
		return create_book(db, book)
	except Exception as e:
		return {"error": str(e)}

@router.get("/books")
def get_all_books_handler(db: SessionLocal = Depends(get_db)):
	try:
		books = get_all_books(db)
		return books
	except Exception as e:
		return {"error": str(e)}

@router.get("/books/{book_id}")
def read_book_handler(book_id: str, db: SessionLocal = Depends(get_db)):
	try:
		book = get_book_by_id(db, book_id)
		if book is None:
			return {"error": "Book not found"}
		return book
	except Exception as e:
		return {"error": str(e)}

@router.put("/books/{book_id}")
def update_book_handler(book_id: str, book: Book, db: SessionLocal = Depends(get_db)):
	try:
		return update_book(db, book_id, book)
	except Exception as e:
		return {"error": str(e)}

@router.delete("/books/{book_id}")
def delete_book_handler(book_id: str, db: SessionLocal = Depends(get_db)):
	try:
		delete_book(db, book_id)
		return "ok"
	except Exception as e:
		return {"error": str(e)}


@router.get("/books/borrowed")
def get_borrowed_books_handler(user_id: str = None, isbn: str = None, book_id: str = None, db: SessionLocal = Depends(get_db)):
	try:
		books = get_borrowed_books(db, user_id, isbn, book_id)
		return books
	except Exception as e:
		return {"error": str(e)}
	
@router.post("/books/borrow/{book_id}/{user_id}")
def borrow_book_handler(book_id: str, user_id: str, db: SessionLocal = Depends(get_db)):
	try:
		return borrow_book(db, user_id, book_id)
	except Exception as e:
		return {"error": str(e)}

@router.put("/books/return/{borrow_id}")
def return_book_handler(borrow_id: str, db: SessionLocal = Depends(get_db)):
	try:
		return return_book(db, borrow_id)
	except Exception as e:
		return {"error": str(e)}