from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import models, session
from app.schemas.book import BookBorrow
from app.schemas.client import ClientCreate


def create_client(db: Session, client: ClientCreate):
    db_client = models.ClientDB(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def link_client_book(db: Session, link_data: BookBorrow):
    db_link = models.BooksClients(**link_data.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def unlink_client_book(db: Session, link_data: BookBorrow):
    db.query(models.BooksClients).filter_by(**link_data.dict()).delete()
    db.commit()


def get_user_by_id(user_id: str, db: Session):
    return db.query(models.ClientDB).filter(models.ClientDB.id == user_id).first()
