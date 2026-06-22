from pydantic import BaseModel, Field, model_validator
from typing import List,Optional
from datetime import date
from fastapi import HTTPException,status



class RegisterSchemas(BaseModel):
    username:str
    name:str
    password:str
    confirm_password:str

    @model_validator(mode="after")
    def password_math(self):
        if self.password != self.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Password do not math"
            )
        return self
    

class Loginschemas(BaseModel):
    username:str
    password:str