from app.core.db_settings  import engine
from app.core.app_setting import setting
from sqlmodel  import Session
from typing  import Annotated
from fastapi  import Depends , HTTPException  , status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from app.models import TokenPayload


# schema_bearer=OAuth2PasswordBearer(tokenUrl=f"{setting.API_V1_STR}/login/access_token")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{setting.API_V1_STR}/login/access_token")
Token_Dep=Annotated[str, Depends(oauth2_scheme)]

def sessionDeepndency():
    with Session(engine)  as session:   
        yield session
        
Get_SESSION=Annotated[Session,Depends(sessionDeepndency)]

def  Decode_Token(token:Token_Dep):
    try:
        payload:dict=jwt.decode(token,setting.SECRET_KEY,algorithms=setting.ALGORITHM)
        
        t_Payload:TokenPayload.PayloadToken=TokenPayload.PayloadToken(**payload) 
        
        if not t_Payload.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token , Id not found in token",
                headers={"WWW-Authenticate":"Bearer"}
            )
        
        if not t_Payload.username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token , username not found in token",
                headers={"WWW-Authenticate":"Bearer"}
            )
        
        return t_Payload           
        
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate":"Bearer"}
        )    
        
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate":"Bearer"}
        ) from e    
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something happend  unexpected in Decoding token in uni profile service {str(e)}"
        ) from e    