from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from app.crud import author
from app.database.session import SessionLocal
from app.schemas.author import Author, AuthorCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/authors", response_model=Author)
def create_author(author_of_book: AuthorCreate, db: Session = Depends(get_db)):
    return author.create_author(db, author_of_book)


@router.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: UUID4, db: Session = Depends(get_db)):
    db_author = author.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.get("/authors", response_model=List[Author])
def get_all_authors(skip: int = 0, limit: int = 10, name_starts_with: Optional[str] = None,
                    db: Session = Depends(get_db)):
    db_author_list = author.get_all_authors(db=db, skip=skip, limit=limit, name_starts_with=name_starts_with)
    if db_author_list is None:
        raise HTTPException(status_code=404, detail="No Author Presents")
    return db_author_list

