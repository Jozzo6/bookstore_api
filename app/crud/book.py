from typing import List
from app.database import SessionLocal
from app.schemas.book import BookBase, Book as BookSchema
from app.models.book import Book


def create_book(db: SessionLocal, book: BookBase) -> BookSchema:
	try:
		db_book = Book(title=book.title, author=book.author)
		db.add(db_book)
		db.commit()
		db.refresh(db_book)
		return BookSchema(**db_book.__dict__)
	except Exception as e:
		db.rollback()
		raise ValueError("An error occurred while creating book: " + str(e))

def get_all_books(db: SessionLocal) -> List[BookSchema]:
	try:
		books = db.query(Book).all()
		return [BookSchema(**book.__dict__) for book in books]
	except Exception as e:
		raise ValueError("An error occurred while fetching books: " + str(e))

def get_book_by_id(db: SessionLocal, book_id: str) -> BookSchema:
	try:
		book = db.query(Book).filter(Book.id == book_id).first()
		return BookSchema(**book.__dict__)
	except Exception as e:
		raise ValueError("An error occurred while fetching book: " + str(e))

def update_book(db: SessionLocal, book_id: str, book: BookSchema) -> BookSchema:
	try:
		db_book = db.query(Book).filter(Book.id == book_id).first()
		db_book.title = book.title
		db_book.author = book.author
		db_book.quantity = book.quantity
		db_book.publisher = book.publisher
		db_book.isbn = book.isbn
		db_book.year = book.year
		db.commit()
		db.refresh(db_book)
		return BookSchema(**db_book.__dict__)
	except Exception as e:
		db.rollback()
		raise ValueError("An error occurred while updating book: " + str(e))
	
def delete_book(db: SessionLocal, book_id: str):
	try:
		db_book = db.query(Book).filter(Book.id == book_id).first()
		db.delete(db_book)
		db.commit()
	except Exception as e:
		db.rollback()
		raise ValueError("An error occurred while deleting book: " + str(e))