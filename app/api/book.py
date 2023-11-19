from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from app.crud import book
from app.database.session import SessionLocal

from app.schemas.book import Book, BookCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/books", response_model=Book)
def create_book(book_to_store: BookCreate, db: Session = Depends(get_db)):
    return book.create_book(db, book_to_store)


@router.get("/books/{book_id}", response_model=Book)
def read_book(book_id: UUID4, db: Session = Depends(get_db)):
    db_book = book.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("/books", response_model=List[Book])
def get_all_books(skip: int = 0, limit: int = 10, title_startswith: Optional[str] = None,
               author_id: Optional[UUID4] = None, db: Session = Depends(get_db)):
    return book.get_books(db, skip=skip, limit=limit, title_startswith=title_startswith, author_id=author_id)
