from typing import List, Optional
from pydantic import BaseModel, UUID4

from app.schemas.author import Author


class BookBase(BaseModel):
    title: str


class BookCreate(BookBase):
    author_id: UUID4


class Book(BookBase):
    id: UUID4
    author: Author

    class Config:
        # orm_mode = True
        from_attributes = True


class BookBorrow(BaseModel):
    is_borrowed: bool
    client_id: UUID4
    book_id: UUID4
