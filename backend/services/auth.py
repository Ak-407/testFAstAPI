from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from utils.config import Config
from fastapi import Depends
from utils.error import raise_exception
from models.users import UsersModel
from db.connection import get_db
from sqlalchemy.orm import Session
from services.users import get_user_service

oauth_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({
        "exp": expire
    })
    encode_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encode_jwt


def get_current_user(token: str = Depends(oauth_schema), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            return raise_exception("Credentials Invalid!", status_code=401)
    except JWTError:
        return raise_exception("Credentials Invalid!", status_code=401)

    um = UsersModel()
    um.email = username
    user = get_user_service(um, db)
    return user
