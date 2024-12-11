from typing import Literal,Annotated
from pydantic_settings import (
    BaseSettings ,
    SettingsConfigDict
)


class Settings(BaseSettings):
    
    model_config  = SettingsConfigDict(
        env_file=".env",env_ignore_empty=True,extra="ignore"
    )
    API_V1_STR:str="/api/v1"
    
    DOMAIN:str="localhost:3000"
    
    PROJECT_NAME:str
    
    DATABASE_URL:str
    # Environment: local, staging, production
    ENVIRONMENT:Literal["local","staging","production"]="local"
    SECRET_KEY:str

    ALGORITHM:str
    
setting=Settings()