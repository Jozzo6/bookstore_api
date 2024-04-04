from app.schemas.user import UserType
import pytest
from unittest.mock import Mock, patch
from app.database import SessionLocal
from app.schemas.book import BookBase, Book as BookSchema
from app.schemas.user import User as UserSchema
from app.models.book import Book
from app.models.user import User
from app.models.users_books import BooksUsers
from app.schemas.borrowed_book import BorrowBook, BorrowBookStatus
from app.crud import book as book_crud

mock_book = Mock(spec=BookSchema, **{
    'title': "Test Book",
    'author': "Test Author",
    'isbn': "1234567890",
    'year': 2021,
    'publisher': "Test Publisher",
    'quantity': 1,
    'id': "1"
})

mock_user = Mock(spec=UserSchema, **{
    'id': "1",
    'email': "test@example.com",
    'first_name': "Test",
    'last_name': "User",
    'type': UserType.admin,
})

mock_borrow_book = Mock(spec=BorrowBook, **{
    'id': "1",
    'book_id': mock_book.id,
    'user_id': mock_user.id,
    'status': BorrowBookStatus.borrowed.value,
    'user': mock_user,
    'book': mock_book,
})

mock_borrow_book_db = Mock(spec=BooksUsers, **{
    'id': "1",
    'book_id': mock_book.id,
    'user_id': mock_user.id,
    'status': BorrowBookStatus.borrowed.value,
    'user': mock_user,
    'book': mock_book,
})

def test_create_book():
    session = SessionLocal()
    mock_book = BookBase(title="Test Book", author="Test Author", quantity=1, publisher="Test Publisher", isbn="1234567890", year=2021)
    with patch.object(session, 'add'), patch.object(session, 'commit'), patch.object(session, 'refresh', side_effect=lambda x: setattr(x, 'id', 1)):
        result = book_crud.create_book(session, mock_book)
    assert result.title == "Test Book"

def test_get_all_books():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_book
    with patch.object(session, 'query', return_value=mock_query), patch.object(session, 'commit'), patch.object(session, 'refresh'):
        result = book_crud.update_book(session, mock_book.id, mock_book)
    assert result.title == mock_book.title

def test_get_book_by_id():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_book
    with patch.object(session, 'query', return_value=mock_query):
        result = book_crud.get_book_by_id(session, mock_user.id)
    assert result.id == mock_user.id

def test_update_book():
    session = SessionLocal()
    mock_book_updated = mock_book
    mock_book_updated.title = "Updated Book"
    mock_db_book = Book(id=mock_book.id, title=mock_book.title, author=mock_book.author, quantity=mock_book.quantity, publisher=mock_book.publisher, isbn=mock_book.isbn, year=mock_book.year)
    with patch.object(session, 'query', return_value=Mock(first=Mock(return_value=mock_db_book))), patch.object(session, 'commit'), patch.object(session, 'refresh'):
        mock_db_book.id = mock_book_updated.id
        result = book_crud.update_book(session, mock_book_updated.id, mock_book_updated)
    assert result.title == "Updated Book"

def test_delete_book():
    session = SessionLocal()
    mock_db_book = Book(id=mock_book.id, title=mock_book.title, author=mock_book.author, quantity=mock_book.quantity, publisher=mock_book.publisher, isbn=mock_book.isbn, year=mock_book.year)
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_db_book
    with patch.object(session, 'query', return_value=mock_query), patch.object(session, 'commit'), patch.object(session, 'delete') as mock_delete:
        book_crud.delete_book(session, mock_db_book.id)
        mock_delete.assert_called_once_with(mock_db_book)

def test_borrow_book():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.side_effect = [mock_book, None]
    mock_query.all.return_value = []
    with patch.object(session, 'query', return_value=mock_query), patch.object(session, 'commit'), patch.object(session, 'refresh'):
        result = book_crud.borrow_book(session, mock_user.id, mock_book.id)
    assert result.book_id == mock_book.id
    assert result.user_id == mock_user.id
    assert result.status == BorrowBookStatus.borrowed.value

def test_borrow_book_user_has_book():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.side_effect = [mock_book, mock_borrow_book]
    mock_query.all.return_value = []
    with patch.object(session, 'query', return_value=mock_query), patch.object(session, 'commit'), patch.object(session, 'refresh'):
        try:
            book_crud.borrow_book(session, mock_user.id, mock_book.id)
        except ValueError as e:
            assert str(e) == "An error occurred while borrowing book: User has already borrowed the book"

def test_borrow_book_no_available_copy():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.side_effect = [mock_book, None]
    mock_query.all.return_value = [mock_book, mock_book]
    with patch.object(session, 'query', return_value=mock_query), patch.object(session, 'commit'), patch.object(session, 'refresh'):
        try:
            book_crud.borrow_book(session, mock_user.id, mock_book.id)
        except ValueError as e:
            assert str(e) == "An error occurred while borrowing book: No available copy of the book"

def test_return_book():
    session = SessionLocal()
    with patch.object(session, 'query', return_value=Mock(first=Mock(return_value=mock_borrow_book_db))), patch.object(session, 'commit'), patch.object(session, 'refresh'):
        result = book_crud.return_book(session, mock_borrow_book_db.id)
    assert result.status == BorrowBookStatus.returned.value

def test_get_borrowed_books():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.options.return_value = mock_query
    mock_query.all.return_value = [mock_borrow_book_db]
    with patch.object(session, 'query', return_value=mock_query):
        result = book_crud.get_borrowed_books(session)
    assert len(result) == 1

def test_get_borrowed_books_by_user_id():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.options.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [mock_borrow_book_db]
    with patch.object(session, 'query', return_value=mock_query):
        result = book_crud.get_borrowed_books(session, user_id=mock_user.id)
    assert len(result) == 1

def test_get_borrowed_books_by_book_id():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.options.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [mock_borrow_book_db]
    with patch.object(session, 'query', return_value=mock_query):
        result = book_crud.get_borrowed_books(session, book_id=mock_book.id)
    assert len(result) == 1

def test_get_no_borrowed_books():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.options.return_value = mock_query
    mock_query.all.return_value = []
    with patch.object(session, 'query', return_value=mock_query):
        result = book_crud.get_borrowed_books(session)
    assert len(result) == 0

def test_get_no_borrowed_books_by_user_id():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.options.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = []
    with patch.object(session, 'query', return_value=mock_query):
        result = book_crud.get_borrowed_books(session, user_id=mock_user.id)
    assert len(result) == 0

def test_get_no_borrowed_books_by_book_id():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.options.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = []
    with patch.object(session, 'query', return_value=mock_query):
        result = book_crud.get_borrowed_books(session, book_id=mock_book.id)
    assert len(result) == 0

def test_delete_borrow():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_borrow_book_db
    with patch.object(session, 'query', return_value=mock_query), patch.object(session, 'commit'), patch.object(session, 'delete') as mock_delete:
        book_crud.delete_borrow(session, "1")
        mock_delete.assert_called_once_with(mock_borrow_book_db)
