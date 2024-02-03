from pydantic import BaseModel
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
        
        
        