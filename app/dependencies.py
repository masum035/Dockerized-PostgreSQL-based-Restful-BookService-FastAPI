from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode

from app.database import session, models
from app.database.session import SessionLocal
from sqlalchemy.orm import Session

from app import schemas
from app.crud import client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "Masum_is_very_dedicated"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(session.get_db)):
    print("Received Token: " + token)
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("Decoded Token: ", payload)
        token_data = schemas.client.TokenData(**payload)
        # print("Type of token_data: ", type(token_data))
        # print("verified Token ", token_data)
        return token_data
    except PyJWTError as e:
        # print("Error decoding token:", e)
        raise credentials_exception


def fetch_client_id_from_token(token: str):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['client_id']
    except PyJWTError as e:
        # print("Error decoding token:", e)
        raise credentials_exception


## Didn't use this method
def get_current_user(token_data: schemas.client.TokenData = Depends(verify_token), db: Session = Depends(session.get_db)):
    print("Type of token_data:", type(token_data))
    print("Content of token_data:", token_data)
    client_id = fetch_client_id_from_token(str(token_data))
    print("Client ID:", client_id)
    user = db.query(models.ClientDB).filter(models.ClientDB.id == client_id).first()
    # user = client.get_user_by_id(db=db, user_id=client_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
