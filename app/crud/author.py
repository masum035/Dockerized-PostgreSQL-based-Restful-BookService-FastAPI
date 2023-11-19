# app/crud/author.py
from typing import Optional

from pydantic import UUID4
from sqlalchemy.orm import Session
from app.database import models
from app.schemas.author import AuthorCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = models.AuthorDB(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: UUID4):
    return db.query(models.AuthorDB).filter(models.AuthorDB.id == author_id).first()


def get_all_authors(db: Session, skip: int = 0, limit: int = 10, name_starts_with: Optional[str] = None):
    query = db.query(models.AuthorDB)
    if name_starts_with:
        query = query.filter(models.AuthorDB.full_name.startswith(name_starts_with))
    return query.offset(skip).limit(limit).all()
