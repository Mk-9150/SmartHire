from sqlmodel import Session  
import jwt 
from jwt.exceptions import InvalidTokenError
from app.core.app_setting import setting
from app.core.db_setting import  engine
from fastapi import Depends, HTTPException, status
from app.models.token import payloadData
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
schema_bearer=OAuth2PasswordBearer(tokenUrl=f"{setting.API_V1_STR}/login/access_token")

Token_Dep=Annotated[str, Depends(schema_bearer)]


def DependencySession():
    with Session(engine) as session:
        yield session
        

Session_Depdnc=Annotated[Session, Depends(DependencySession)]



def TokenDependency(token:Token_Dep):
    ...      
    try:
        ...
        payload=jwt.decode(token,setting.SECRET_KEY,algorithms=setting.ALGORITHM)
        
        print(payload)
        data:payloadData=payloadData(**payload)
        
        if not data.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token , Id not found in token",
                headers={"WWW-Authenticate":"Bearer"}
            )
        
        if not data.username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token , username not found in token",
                headers={"WWW-Authenticate":"Bearer"}
            )
        
        return data        
                    
        
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate":"Bearer"}
        ) from e      
    
        
get_TokenData=Annotated[payloadData, Depends(TokenDependency)] 

