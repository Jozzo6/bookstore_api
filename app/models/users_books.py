import uuid
from app.database import Base
from sqlalchemy import Column, String, DateTime, func, ForeignKey, Text

class BooksUsers(Base):
	__tablename__ = 'users_books'
	
	id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
	created = Column(DateTime, default=func.now())
	updated = Column(DateTime, default=func.now(), onupdate=func.now())
	user_id = Column(ForeignKey('users.id'), nullable=False)
	book_id = Column(ForeignKey('books.id'), nullable=False)
	status = Column(String, nullable=False)
