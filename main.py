from fastapi import FastAPI , Depends , HTTPException , status
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from models import User
from database import get_db , metadata , engine, Base
from sqlalchemy.orm import Session
from auth import get_current_user , pwd_context , create_access_token , verify_password ,ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserCreate  , Token , UserLogin , UserResponse
from typing import List , Annotated
from models import User
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)
app = FastAPI() 

db_dependency = Annotated[Session,Depends(get_db)]



@app.post("/users/" ,  )
def create_user(user:UserCreate , db:db_dependency):
    try:
        password =  pwd_context.hash(user.password)
        new_user =  User( fullname=user.full_name,username=user.username , hashed_password=password) 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
    
@app.post("/token", response_model=Token)
async def  login(db:db_dependency,cred: OAuth2PasswordRequestForm=Depends() ):
    try:
        user = db.query(User).filter(User.username == cred.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Invalid Credentials")
        if not verify_password(cred.password , user.hashed_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Invalid Credentials")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
    
@app.get("/users/me/" , response_model=UserResponse  )
async def get_current_user (current_user:User = Depends(get_current_user)):
     try:
            return UserResponse(id=current_user.id , username=current_user.username , full_name=current_user.fullname)
     except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
    