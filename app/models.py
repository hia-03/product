from sqlalchemy import Column,Integer,String,Date,ForeignKey,Table,DateTime,Boolean,Enum as SqlEnum,UniqueConstraint,Text,Float
from sqlalchemy.orm import DeclarativeBase,relationship
import enum
from datetime import datetime


class BaseModel(DeclarativeBase):
    pass


class UserModel(BaseModel):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100),unique=True)
    name = Column(String(100))
    password = Column(String(100))
    is_superuser = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.utcnow)

    products = relationship("Product",back_populates="owner")
    refreshtok = relationship("RefreshToken", back_populates="userid")



class Product(BaseModel):
    __tablename__ = "product"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    title = Column(String(100))
    description = Column(String(255))
    price = Column(Float)
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    owner = relationship("UserModel",back_populates="products")



class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    token = Column(String(255),unique=True)
    expires_at = Column(DateTime,nullable=False)

    userid = relationship("UserModel",back_populates="refreshtok")