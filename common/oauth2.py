from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

#pip install python-jose
#SECRET_KEY - imported from .env
#ALGORYTHM
#EXP_TIME = 30 minutes


SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORYTHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)

    return encoded_jwt


