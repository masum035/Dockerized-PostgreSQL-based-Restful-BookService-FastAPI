from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base

DATABASE_URL = "postgresql://Masum:Masum044@localhost/BookService"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
