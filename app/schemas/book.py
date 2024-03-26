from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookBase(BaseModel):
	title: str
	author: str
	isbn: str
	year: int
	publisher: str
	quantity: int

class Book(BookBase):
	id: str
	created: Optional[datetime]
	updated: Optional[datetime]

	class Config:
		orm_mode = True