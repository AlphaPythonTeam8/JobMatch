from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from data import schemas

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# pip install python-jose
# SECRET_KEY - imported from .env
# ALGORYTHM
# EXP_TIME = 30 minutes


SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORYTHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
        id: str = payload.get("company_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
