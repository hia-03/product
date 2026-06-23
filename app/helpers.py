from passlib.hash import pbkdf2_sha256
from fastapi import Depends,HTTPException,status
from db_config import SessionLocal
from .models import *

def hash_password(password:str):
    password_hash = pbkdf2_sha256.hash(password)
    return password_hash


def verify_password(password:str,password_hash:str):
    return pbkdf2_sha256.verify(password,password_hash)


def check_owner_and_ownerproduct(product,current_user):
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You dont have permission"
        ) 
    
    return True


def is_superusers(user: UserModel):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin Only"
        )