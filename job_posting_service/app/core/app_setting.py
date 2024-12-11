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
    SCHEMA_REGISTRY_URL:str
    Topic_Applier:str
    PROJECT_NAME:str
    BOOTSTRAP_SERVER_KAFKA_URL:str
    DATABASE_URL:str
    # Environment: local, staging, production
    ENVIRONMENT:Literal["local","staging","production"]="local"
    SECRET_KEY:str
    
    

    ALGORITHM:str
    
setting=Settings()