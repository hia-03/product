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