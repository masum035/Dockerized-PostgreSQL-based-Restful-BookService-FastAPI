from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.crud import client
from app.database import models, session
from app.database.session import SessionLocal
from app.dependencies import create_access_token, oauth2_scheme, verify_token, \
    fetch_client_id_from_token
from app.schemas.book import Book, BookBorrow

from app.schemas.client import ClientCreate, ClientResponse, TokenData

router = APIRouter()


@router.post("/clients", response_model=ClientResponse)
def create_client(client_to_borrow: ClientCreate, db: Session = Depends(session.get_db)):
    db_client = client.create_client(db, client_to_borrow)
    token_data = {"sub": str(db_client.full_name), "client_id": str(db_client.id)}
    access_token = create_access_token(token_data)
    return {"id": str(db_client.id), "full_name": db_client.full_name, "access_token": access_token,
            "token_type": "bearer"}
    # return {"access_token": access_token, "token_type": "bearer"}


@router.post("/clients/{client_id}/link_book/{book_id}")
def link_client_book(client_id: UUID4, book_id: UUID4, db: Session = Depends(session.get_db)):
    link_data = BookBorrow(client_id=client_id, book_id=book_id, is_borrowed=True)
    try:
        borrowed_book = client.link_client_book(db, link_data)
        return borrowed_book
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Book already borrowed by the client")


@router.delete("/clients/{client_id}/unlink_book/{book_id}")
def unlink_client_book(client_id: UUID4, book_id: UUID4, db: Session = Depends(session.get_db)):
    link_data = BookBorrow(client_id=client_id, book_id=book_id, is_borrowed=True)
    return client.unlink_client_book(db, link_data)



@router.get("/clients/books_borrowed_by_client", response_model=List[Book])
def books_borrowed_by_client(token: str = Depends(oauth2_scheme), db: Session = Depends(session.get_db)):
    verify_token(token)
    client_id = fetch_client_id_from_token(str(token))
    user = db.query(models.ClientDB).filter(models.ClientDB.id == client_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    client_id = user.id

    return db.query(models.BookDB).join(models.BooksClients).filter(models.BooksClients.client_id == client_id).all()
