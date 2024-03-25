import uuid
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlalchemy import Column, String, DateTime, func, ForeignKey

class BooksUsers(Base):
	__tablename__ = 'users_books'
	
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("(gen_random_uuid())"))
	created = Column(DateTime, default=func.now())
	updated = Column(DateTime, default=func.now(), onupdate=func.now())
	user_id = Column(ForeignKey('users.id'), nullable=False)
	book_id = Column(ForeignKey('books.id'), nullable=False)
	status = Column(String, nullable=False)
	another_column = Column(String, nullable=False)
