from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, UUID4


class ClientBase(BaseModel):
    full_name: str


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: UUID4

    class Config:
        # orm_mode = True
        from_attributes = True


class ClientResponse(Client):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str
    exp: int
    client_id: str
