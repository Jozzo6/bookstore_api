from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BorrowBookStatus(Enum):
	borrowed = "borrowed"
	returned = "returned"

class BorrowBookBase(BaseModel):
	book_id: int
	user_id: int
	status: str

class BorrowBook(BorrowBookBase):
	id: int
	created: Optional[datetime]
	updated: Optional[datetime]

	class Config:
		orm_mode = True