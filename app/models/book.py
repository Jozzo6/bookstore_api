import uuid
from app.database import Base
from sqlalchemy import Column, Integer, DateTime, func, Text

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
    title = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    publisher = Column(Text, nullable=False)
    isbn = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
