# jwt_authentication_fastapi
 JWT authenication in fastapi


## Description
This is a simple fastapi application that demonstrates how to use JWT for authentication. It has a simple user registration and login system. The user is authenticated using JWT and the token is used to access protected routes.



## Installation

### Clone the repository
```bash
git clone 'repository url'
cd jwt_authentication_fastapi
```
### Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
### Install the requirements

```bash
pip install -r requirements.txt


```
### Run the application
```bash
uvicorn main:app --reload
```

## Explaining the code
The code is divided into 3 main parts:
1. User model and database
2. JWT authentication
3. Routes


### User model and database
The user model is defined in the `models.py` file. It is a simple model with 4 fields: `id`, `username` , `fullname` and `password`. The `id` field is the primary key and is autoincremented. The `username` field is a string and is unique. The `password` field is also a string and is hashed using `bcrypt` before being stored in the database.

### model

```bash
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    fullname = Column(String)
    password = Column(String)
```

### schemas
The model schemas as defined in the `schemas.py` file. The `UserCreate` schema is used for user registration and the `UserResponse` schema is used to return the user details after registration and login. Token schema is used to return the JWT token after login.
```bash
from typing import List, Optional


class UserCreate(BaseModel):
    username: str
    full_name :str
    password:str
    
class UserLogin(BaseModel):
    username: str
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class UserResponse(BaseModel):
    id:int
    username:str
    full_name:str
    class Config:
        orm_mode = True

```

### JWT authentication
The JWT authentication is implemented in the `auth.py` file. The `create_access_token` function is used to create the JWT token. The `get_current_user` function is used to get the current user from the JWT token. The `get_password_hash` function is used to hash the password before storing it in the database. The `verify_password` function is used to verify the password during login.

### auth.py

#### constants
Note that the `SECRET_KEY` and `ALGORITHM` are  should be stored in a `.env` file and not hardcoded in the code.

```bash
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```


### create_access_token
```bash
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 
    ```

### get_current_user
```bash
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

```