from typing import Optional

from pydantic import UUID4
from sqlalchemy.orm import Session
from app.database import models
from app.schemas.book import BookCreate


def create_book(db: Session, book: BookCreate):
    db_book = models.BookDB(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: UUID4):
    return db.query(models.BookDB).filter(models.BookDB.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10, title_startswith: Optional[str] = None,
              author_id: Optional[UUID4] = None):
    query = db.query(models.BookDB)
    if title_startswith:
        query = query.filter(models.BookDB.title.startswith(title_startswith))
    if author_id:
        query = query.filter(models.BookDB.author_id == author_id)
    return query.offset(skip).limit(limit).all()
