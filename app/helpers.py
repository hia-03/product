from passlib.hash import pbkdf2_sha256
from fastapi import Depends
from db_config import SessionLocal
from .models import *

def hash_password(password:str):
    password_hash = pbkdf2_sha256.hash(password)
    return password_hash


def verify_password(password:str,password_hash:str):
    return pbkdf2_sha256.verify(password,password_hash)