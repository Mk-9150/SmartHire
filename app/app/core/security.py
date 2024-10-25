from  passlib.context import CryptContext
from app.core.settings import setting
from typing import Union,Annotated
from datetime import datetime , timezone , timedelta
from fastapi.security import OAuth2PasswordBearer 
from fastapi import Depends
import jwt


bearer_Schema=OAuth2PasswordBearer(tokenUrl="/institute/login")


token=Annotated[Depends , bearer_Schema]


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

 
# def createToken(*,data:dict[str,Union[int | str ]],expires=timedelta(days=1)):
def createToken(*,data:dict[str,Union[int | str ]],expires:timedelta|None=None):
    to_encode=data.copy()
    
    if expires :
        expires_in=datetime.now(timezone.utc) + expires 
        expires_in_str = expires_in.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:     
        expires_in=datetime.now(timezone.utc) + timedelta(days=1) 
        expires_in_str = expires_in.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    to_encode.update({"expiresTime":expires_in_str})
     
    
    
    return jwt.encode(to_encode , setting.KEY , algorithm="HS256")
    
    



def  get_hashed_Password(password:str):
   return pwd_context.hash(password)


def verify_password(password:str,hashPass:str):
    return pwd_context.verify(password,hashPass)
    
    