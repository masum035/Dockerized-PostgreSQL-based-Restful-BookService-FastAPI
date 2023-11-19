from typing import List
from pydantic import BaseModel, UUID4


class AuthorBase(BaseModel):
    full_name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: UUID4

    class Config:
        # orm_mode = True,
        from_attributes = True

