from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
    )

import secrets

from pydantic import(
    model_validator , 
    BeforeValidator ,
    computed_field,
    
)
from datetime import datetime , timedelta


from typing import Annotated
from app.core.utils import parse_cors


class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file='.env' , env_ignore_empty=True,extra="ignore"
    )
    
    API_V1_STR:str="/api/v1"
    
    KEY:str=secrets.token_urlsafe(32)
    
    # TOKEN_EXPIRES_TIME:timedelta = timedelta(days=1)
    TOKEN_EXPIRES_TIME:int = 60*24*1  # 1 day 
    
    PROJECT_NAME:str
    DESCRIPTION:str
    ENV:str
    
    DATABASE_URL:str
    
    BACKEND_CORS_ORIGINS:Annotated[list[str] | str , BeforeValidator(parse_cors)]
    
    
     
    
    
    
setting=Settings()
    
    