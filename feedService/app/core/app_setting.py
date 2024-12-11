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
    
    POST_SERVICE_URL:str
    BOOTSTRAP_SERVER_KAFKA_URL:str
    DATABASE_URL:str
    # Environment: local, staging, production
    ENVIRONMENT:Literal["local","staging","production"]="local"
    SECRET_KEY:str
    KAFKA_TOPIC_FOLLOW:str
    KAFKA_TOPIC_FOLLOW_BACK:str
    KAFKA_TOPIC_UN_FOLLOW:str
    SCHEMA_REGISTRY_URL:str
    KAFKA_TOPIC_Account_Created:str
    ALGORITHM:str
    KAFKA_TOPIC_POST_CREATED:str
    Topic_Applier:str
    
setting=Settings()