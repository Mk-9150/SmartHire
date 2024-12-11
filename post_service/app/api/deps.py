
from sqlmodel import Session , SQLModel , select
from typing import Annotated , Union , Any
from fastapi import Depends , HTTPException,Header,status
import requests
from app.core.db_setting import engine 
from aiokafka import AIOKafkaProducer
from app.core.app_settings import setting
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer

schema_bearer=OAuth2PasswordBearer(tokenUrl=f"{setting.API_V1_STR}/login/access_token")
Token_Bearer=Annotated[str, Depends(schema_bearer)]
from app.Models import TokenPayload_model


def sessionDependency():
    with Session(engine) as session:
        yield session
        ...

session_Dep=Annotated[Session,Depends(sessionDependency)]        


def DecodeToken_AND_get_user(token:Annotated[str,Header()]):
     ...
     
     url="http://localhost:8002/currentuser"  #  the URL For user management service to get current user
     headers = {
            'Authorization': f'Bearer {token}',  # Include the token in the Authorization header
            'Content-Type': 'application/json'   # Set the content type, typically 'application/json'
         }
     
     response=requests.post(url=url,headers=headers)
     if response.status_code==200:
         print("Request was successful!")
         # print(response.json())  # or response.text if it's not JSON
         return response.json()
     
     else :
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,detail="request not successfull in token dependency  create post" 
          )
     

tokenDep=Annotated[Any,Depends(DecodeToken_AND_get_user)]


def tokenDepedency2(token:Token_Bearer):
    ...
    try:
         ...
         payload=jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
         print(payload)
         TokenData:TokenPayload_model.TokenPayload=TokenPayload_model.TokenPayload(**payload)
         
         if not TokenData.id:
             raise HTTPException(
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Invalid Token",
                 headers={"WWW-Authenticate":"Bearer"}
             )
         
         if not TokenData.username:
             raise HTTPException(
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Invalid Token",
                 headers={"WWW-Authenticate":"Bearer"}
             )
          
         return TokenData       

    except  InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate":"Bearer"}
        ) from e    
         
    except  Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate":"Bearer"}
        ) from e    

GET_TOKEN_Data=Annotated[TokenPayload_model.TokenPayload,Depends(tokenDepedency2)]


async def get_kafka_producer():
       #    producer=AIOKafkaProducer(bootstrap_servers=setting.BOOTSTRAP_SERVER_KAFKA_URL , acks=all)
        producer=AIOKafkaProducer(bootstrap_servers=setting.BOOTSTRAP_SERVER_KAFKA_URL )
        await producer.start()
        try:
            yield producer
        finally:
            await producer.stop() 

kafka_producer=Annotated[AIOKafkaProducer,Depends(get_kafka_producer)]            
            








# def tokenValidity(token:Annotated[str,Depends(oauth2_bearer)],session:common_Session):
#     try:
#         _:bool=load_dotenv(find_dotenv())
#         SECRET_KEY:str=getenv("SECRET_KEY","not found")
#         ALGORITHM:str=getenv("ALGORITHM", "not found")
#         payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         # return payload
#         username:Any|None=payload.get("username")  # str
#         id:Any|None=payload.get("id")  # int 
#         if username is None or id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#         teacher:Teacher|None=session.get(Teacher, id)
#         if teacher is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#         return teacher
#     except:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")   