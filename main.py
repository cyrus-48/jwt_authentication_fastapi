from fastapi import FastAPI , Depends , HTTPException , status
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from models import User
from database import get_db 
from sqlalchemy.orm import Session
from auth import get_current_user , pwd_context , create_access_token , verify_password ,ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserCreate  , Token , UserLogin , UserResponse , NoteCreate , NoteResponse
from typing import List , Annotated
from models import User , Note
from datetime import datetime, timedelta 
from typing import List
app = FastAPI() 

db_dependency = Annotated[Session,Depends(get_db)]

auth_dependency = Annotated[User,Depends(get_current_user)]



@app.post("/users/" ,  )
def create_user(user:UserCreate , db:db_dependency):
    try:
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Username already exists")
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
        
@app.post("/notes/" , response_model=NoteResponse )
async def  create_note(note:NoteCreate , db:db_dependency , curr_user:auth_dependency):
    try:
       new_note  = Note(title=note.title , description=note.description , owner_id=curr_user.id)
       db.add(new_note)
       db.commit()
       db.refresh(new_note)
       db.query(User).filter(User.id==curr_user.id).first()
       owner = UserResponse(id=curr_user.id,username=curr_user.username ,full_name=curr_user.fullname)
       data = {
           "title":new_note.title,
           "description":new_note.description,
           "created_at":new_note.created_at,
           "updated_at":new_note.updated_at,
           "is_deleted":new_note.is_deleted,
           "owner_id":new_note.owner_id,
           "owner": owner,
           "id":new_note.id
           
       }
       return  NoteResponse(**data)
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
   
   
    
   
@app.get("/notes/me/")
async def get_all_notes(db:db_dependency ,  curr_user:auth_dependency):
    try:
        notes = db.query(Note).filter(Note.owner_id == curr_user.id).all()
        return notes
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
    
    
@app.get("/notes/{note_id}/" , response_model=NoteResponse)
async def get_note_by_id(note_id:int , db:db_dependency , curr_user:auth_dependency):
    try:
        note = db.query(Note).filter(Note.id == note_id , Note.owner_id == curr_user.id).first()
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Note not found")
        owner = UserResponse(id=curr_user.id,username=curr_user.username ,full_name=curr_user.fullname)
        data = {
           "title":note.title,
           "description":note.description,
           "created_at":note.created_at,
           "updated_at":note.updated_at,
           "is_deleted":note.is_deleted,
           "owner_id":note.owner_id,
           "owner": owner,
           "id":note.id
           
       }
        return  NoteResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
    
@app.put("/notes/{note_id}/" , response_model=NoteResponse)
async def update_note_by_id(note_id:int , note:NoteCreate , db:db_dependency , curr_user:auth_dependency):
    try:
        note = db.query(Note).filter(Note.id == note_id , Note.owner_id == curr_user.id).first()
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Note not found")
        note.title = note.title
        note.description = note.description
        db.commit()
        db.refresh(note)
        owner = UserResponse(id=curr_user.id,username=curr_user.username ,full_name=curr_user.fullname)
        data = {
           "title":note.title,
           "description":note.description,
           "created_at":note.created_at,
           "updated_at":note.updated_at,
           "is_deleted":note.is_deleted,
           "owner_id":note.owner_id,
           "owner": owner,
           "id":note.id
           
       }
        return  NoteResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
    
    
@app.delete("/notes/{note_id}/" , response_model=NoteResponse)
async def delete_note_by_id(note_id:int , db:db_dependency , curr_user:auth_dependency):
    try:
        note = db.query(Note).filter(Note.id == note_id , Note.owner_id == curr_user.id).first()
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Note not found")
        note.is_deleted = True
        db.commit()
        db.refresh(note)
        owner = UserResponse(id=curr_user.id,username=curr_user.username ,full_name=curr_user.fullname)
        data = {
           "title":note.title,
           "description":note.description,
           "created_at":note.created_at,
           "updated_at":note.updated_at,
           "is_deleted":note.is_deleted,
           "owner_id":note.owner_id,
           "owner": owner,
           "id":note.id
           
       }
        return  NoteResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
    
    
    
   

    