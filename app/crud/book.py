from typing import List
import uuid
from app.database import SessionLocal
from app.schemas.book import BookBase, Book as BookSchema
from app.schemas.borrowed_book import BorrowBook, BorrowBookStatus
from app.models.book import Book
from app.models.users_books import BooksUsers
from sqlalchemy.orm import joinedload

def create_book(db: SessionLocal, book: BookBase) -> BookSchema:
	try:
		db_book = Book(title=book.title, author=book.author, quantity=book.quantity, publisher=book.publisher, isbn=book.isbn, year=book.year)
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
	
def borrow_book(db: SessionLocal, user_id: str, books_id: str) -> BorrowBook:
	try:
		book = db.query(Book).filter(Book.id == books_id).first()
		if book.quantity <= 0:
			raise ValueError("No available copy of the book")
		book_user = db.query(BooksUsers).filter(BooksUsers.user_id == user_id, BooksUsers.book_id == books_id, BooksUsers.status == BorrowBookStatus.borrowed.value).first()
		if book_user:
			raise ValueError("User has already borrowed the book")

		books = db.query(BooksUsers).filter(BooksUsers.book_id == books_id, BooksUsers.status == BorrowBookStatus.borrowed.value).all()
		if len(books) >= book.quantity:
			raise ValueError("No available copy of the book")
		
		book_user = BooksUsers(id=str(uuid.uuid4()), user_id=user_id, book_id=books_id, status=BorrowBookStatus.borrowed.value)
		db.add(book_user)
		db.commit()
		db.refresh(book_user)
		return BorrowBook(**book_user.__dict__)
	except Exception as e:
		db.rollback()
		raise ValueError("An error occurred while borrowing book: " + str(e))

def return_book(db: SessionLocal, borrow_id: str) -> BorrowBook:
	try:
		book_user = db.query(BooksUsers).filter(BooksUsers.id == borrow_id).first()
		if not book_user:
			raise ValueError("User has not borrowed the book")
		book_user.status = BorrowBookStatus.returned.value
		db.commit()
		db.refresh(book_user)
		return BorrowBook(**book_user.__dict__)
	except Exception as e:
		db.rollback()
		raise ValueError("An error occurred while deleting book: " + str(e))

def get_borrowed_books(db: SessionLocal, user_id: str = None, isbn: str = None, book_id: str = None) -> List[BorrowBook]:
    try:
        query = db.query(BooksUsers).options(joinedload(BooksUsers.book), joinedload(BooksUsers.user))

        if user_id:
            query = query.filter(BooksUsers.user_id == user_id)
        if isbn:
            query = query.filter(BooksUsers.book.has(Book.isbn == isbn))
        if book_id:
            query = query.filter(BooksUsers.book_id == book_id)

        books = query.all()

        return [BorrowBook(**book.__dict__) for book in books if book is not None]
    except Exception as e:
        raise ValueError("An error occurred while fetching books: " + str(e))
	
def delete_borrow(db: SessionLocal, borrow_id: str):
	try:
		book_user = db.query(BooksUsers).filter(BooksUsers.id == borrow_id).first()
		if not book_user:
			raise ValueError("User has not borrowed the book")
		db.delete(book_user)
		db.commit()
	except Exception as e:
		db.rollback()
		raise ValueError("An error occurred while deleting book: " + str(e))