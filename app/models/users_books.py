import uuid
from app.database import Base
from sqlalchemy import Column, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship

class BooksUsers(Base):
	__tablename__ = 'users_books'
	
	id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
	created = Column(DateTime, default=func.now())
	updated = Column(DateTime, default=func.now(), onupdate=func.now())
	user_id = Column(ForeignKey('users.id'), nullable=False)
	book_id = Column(ForeignKey('books.id'), nullable=False)
	status = Column(Text, nullable=False)

	user = relationship('User', back_populates='users_books')
	book = relationship('Book', back_populates='users_books')
