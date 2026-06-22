from fastapi import APIRouter,Depends,HTTPException,FastAPI,Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from db_config import get_db
from .models import *
from .schemas import *
from .helpers import *
from .auth import *
account = APIRouter()




@account.post("/register",tags=['auth'])
def register_accounts(request:Request,data:RegisterSchemas,db:Session = Depends(get_db)):

    oldusername = db.query(UserModel).filter(UserModel.username == data.username).first()
    if oldusername:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already exist'
        )
    
    pas_hash = hash_password(data.password)
    user = UserModel(username=data.username,name=data.name,password=pas_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message":"register successfully"}



@account.post("/login",tags=['auth'])
def login_view(data:)