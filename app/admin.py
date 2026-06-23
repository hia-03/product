from fastapi import APIRouter,Depends,HTTPException,FastAPI,Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from db_config import get_db
from datetime import datetime, timedelta
from .models import *
from .schemas import *
from .helpers import *
from .auth import *


adminn = APIRouter()


@adminn.get("/admin/products",tags=['admin'])
def get_all_products_admin(
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    
    is_superusers(current_user)

    res = db.query(Product).all()

    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found"
        )
    
    return res

@adminn.get("/admin/users",tags=['admin'])
def get_all_users(
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    is_superusers(current_user)
    
    users = db.query(UserModel).all()

    result = []

    for user in users:
        result.append({
            "id":user.id,
            "username":user.username,
            "name":user.name,
            "is_superuser":user.is_superuser,
            "created_at":user.created_at
        })

    return result

@adminn.delete("/admin/deluser/{user_id}",tags=['admin'])
def del_user_by_admin(
    user_id:int,
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    is_superusers(current_user)

    users = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found"
        )
    
    db.delete(users)
    db.commit()
    return {
        "message": f"Id User {user_id} Deleted successfully by admin"
    }


@adminn.put("/admin/updateproduct/{product_id}",tags=['admin'])
def upda_by_admin(
    product_id:int,
    data:ProductsSchemas,
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    is_superusers(current_user)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    product.title = data.title
    product.description = data.description
    product.price = data.price

    db.commit()
    db.refresh(product)

    return {
        "message": "Product updated successfuly by admin",
        "product":product
    }

@adminn.delete("/admin/deleteproduct/{product_id}",tags=['admin'])
def delproduct_by_admin(
    product_id:int,
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    is_superusers(current_user)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully by admin"
    }