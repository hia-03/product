import time
from typing import Dict
import jwt
from decouple import config
from dotenv import load_dotenv
from fastapi import HTTPException, Request, Depends, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models import *
from db_config import get_db

import os


load_dotenv()


JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITM")
security = HTTPBearer()

def token_response(token : str):
    return {
        "access_token": token
    }

def sign_jwt (user_email:str):
    payload = {
        "user_id": user_email,
        "expires": time.time() + 60
    } 
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {
        "access_token": token
    }


def verify_jwt(token: str, db: Session = Depends(get_db)):
    try:
        refresh  = db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if not refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        payload = jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])

        if payload['expires'] < time.time():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token has expired"
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
    

def jwt_required(
        credentials:HTTPAuthorizationCredentials = Depends(security),
        db:Session = Depends(get_db)
        ):
    token = credentials.credentials
    return verify_jwt(token,db=db)


def get_current_user(
        payload: dict = Depends(jwt_required),
        db:Session = Depends(get_db)) -> UserModel:
    user_email = payload("user_id")
    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate credentials" 
        )
    
    user = db.query(UserModel).filter(UserModel.username == user_email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "User Not Found" 
        )
    
