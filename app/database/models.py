import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class AuthorDB(Base):
    __tablename__ = "authors"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    full_name = Column(String, index=True)
    books = relationship("BookDB", back_populates="author")


class BookDB(Base):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.id"))
    author = relationship("AuthorDB", back_populates="books")


class ClientDB(Base):
    __tablename__ = "clients"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    full_name = Column(String, index=True)
    books = relationship("BookDB", secondary="books_clients")


class BooksClients(Base):
    __tablename__ = "books_clients"
    is_borrowed = Column(Boolean, default=False, index=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), primary_key=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), primary_key=True)
