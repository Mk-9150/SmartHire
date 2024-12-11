from sqlmodel import Session 
from app.core.db_settings import engine
from fastapi import Depends
from typing import Annotated ,Any
from fastapi.security import OAuth2PasswordBearer
from app.core.app_setting import setting
from fastapi import HTTPException , status
import  jwt
from jwt.exceptions import InvalidTokenError
from app.models.payloadToken import TokenPayload


schema_bearer=OAuth2PasswordBearer(tokenUrl=f"{setting.API_V1_STR}/login/access_token")
Token_Dep=Annotated[str,Depends(schema_bearer)]


def Session_Depecdency():
    
    with Session(engine) as session:
        yield session

GET_SESSION=Annotated[Session,Depends(Session_Depecdency)]        


def Decode_token(token:Token_Dep):
    ...
    try:
        ... 
             
        payload=jwt.decode(token,setting.SECRET_KEY,algorithms=setting.ALGORITHM)
        print(payload)
        data:TokenPayload=TokenPayload(**payload)
        
        if not data.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token , Id not found in Token",
                headers={"WWW-Authenticate":"Bearer"}
            )
                   
        if not data.username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token , username not found in Token",
                headers={"WWW-Authenticate":"Bearer"}
            )           
        
        return data    
        
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate":"Bearer"}
        ) from e
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate":"Bearer"}
        ) from e    
    
    
GET_TOKEN_DATA=Annotated[Any,Depends(Decode_token)]    
    