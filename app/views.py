from fastapi import APIRouter,Depends,HTTPException,FastAPI,Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from db_config import get_db
from datetime import datetime, timedelta
from .models import *
from .schemas import *
from .helpers import *
from .auth import *
from .pagination import *
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
def login_view(data:Loginschemas,db:Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == data.username).first()
    if not user or not verify_password(data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = sign_jwt(user.username)
    refresh_token = RefreshToken(
    user_id=user.id,
    token=token["access_token"],
    expires_at=datetime.utcnow() + timedelta(days=7)
)
    db.add(refresh_token)
    db.commit()
    
    return token



@account.post("/logout",tags=['auth'])
def logout_view(db:Session = Depends(get_db),credentials:HTTPAuthorizationCredentials=Depends(security)):
    jwt_token = credentials.credentials
    print(jwt_token)
    
    refresh_token = db.query(RefreshToken).filter(RefreshToken.token == jwt_token).first()
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found"
        )
    print(refresh_token)
    db.delete(refresh_token)
    db.commit()
    print(refresh_token)

    return {
        "message":"Logged out successfully"
    }
##
@account.get("/products/search", tags=['product'])
def search_product(
    title:str,
    db:Session = Depends(get_db)
):
    products = db.query(Product).filter(Product.title.contains(title)).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return products


@account.get("/product/bypage", tags=['product'])
def gett_product(
    page:int = 1,
    db:Session = Depends(get_db)
):
    offset,limit = pagination(page,4)

    products = db.query(Product).offset(offset).limit(limit).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    

    return {
        "page": page,
        "limit": 4,
        "data": products
    }


# //

@account.post("/add-product",tags=['products'])
def add_product(data:ProductsSchemas,db:Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    print("rizooo")
    print(current_user.id)
    print(current_user.id)
    print("rizo")
    product = Product(
        title = data.title,
        description = data.description,
        price = data.price,
        owner_id = current_user.id
    )
    db.add(product)
    db.commit()
    print(current_user.id)


    return {
        "message": f"Product created Product name {product.title}"
    }


@account.get("/product/{product_id}",tags=['products'])
def get_product_by_id(
    product_id: int,
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)):
    
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    check_owner_and_ownerproduct(product,current_user)

    return product




@account.put("/product/up/{product_id}",tags=['products'])
def update_product_by_id(
    product_id: int,
    data: ProductsSchemas,
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    check_owner_and_ownerproduct(product,current_user)

    product.title = data.title
    product.description = data.description
    product.price = data.price

    db.commit()
    db.refresh(product)

    return {
        "message": f"Product {product_id} update successfully"
    }

@account.delete("/product/del/{product_id}",tags=['products'])
def delete_product_by_id(
    product_id: int,
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    check_owner_and_ownerproduct(product,current_user)

    db.delete(product)
    db.commit()

    return {
        "message": f"Product {product_id} deleted succesfully"
    }
    

@account.get("/all-product",tags=['products'])
def get_my_product(
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    products = db.query(Product).filter(Product.owner_id == current_user.id).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return products

#// dlya polzovateley

@account.get("/all-products",tags=['product'])
def  get_all_product(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return products





@account.get("/products/{products_id}",tags=['product'])
def get_id_products(
    products_id:int,
    db:Session = Depends(get_db)
):
    products = db.query(Product).filter(Product.id == products_id).first()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return products

