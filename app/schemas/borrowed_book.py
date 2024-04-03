from enum import Enum
from app.schemas.book import Book
from app.schemas.user import User
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BorrowBookStatus(Enum):
	borrowed = "borrowed"
	returned = "returned"

class BorrowBookBase(BaseModel):
	book_id: str
	user_id: str
	status: str

class BorrowBook(BorrowBookBase):
	id: str
	user: Optional[User]
	book: Optional[Book]
	created: Optional[datetime]
	updated: Optional[datetime]

	class Config:
		orm_mode = True