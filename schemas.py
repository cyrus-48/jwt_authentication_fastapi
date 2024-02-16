from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


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
        
        
class NoteCreate(BaseModel):
    title:str
    description:str
    
class NoteResponse(NoteCreate):
    created_at:datetime
    updated_at:None | datetime
    is_deleted:bool
    owner_id:int
    owner:UserResponse
    id:int 
    
    class config:
        orm_mode = True
        
        