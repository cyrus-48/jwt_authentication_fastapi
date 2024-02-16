from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from database import get_db
from models import User
from sqlalchemy.orm import Session
from fastapi import Depends

# hashing the password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "JFDSGHFUIEWHIUHDF8Q97R389U903UR8Y98fyhqghsf98ufuyf90u28920"

ALGORITHM = "HS256" 

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 30 
#verify password
def verify_password(plain_password, hashed_password)->bool:
    return pwd_context.verify(plain_password, hashed_password)


# create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 


def get_current_user(db:Session = Depends(get_db) , access_token:str = Depends(oauth2_schema)):
    credentials_exception = JWTError
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


