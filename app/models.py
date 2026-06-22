from sqlalchemy import Column,Integer,String,Date,ForeignKey,Table,DateTime,Boolean,Enum as SqlEnum,UniqueConstraint,Text
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



class Product(BaseModel):
    __tablename__ = "product"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    title = Column(String(100))
    description = Column(String(255))
    price = Column(float)
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    owner = relationship("UserModel",back_populates="products")