from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum

class UserType(Enum):
    admin = 3
    librarian = 2
    user = 1
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    type: UserType

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created: Optional[datetime]
    updated: Optional[datetime]

    class Config:
        orm_mode = True