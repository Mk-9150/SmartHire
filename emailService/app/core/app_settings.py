from pydantic import (
    model_validator ,
    BeforeValidator ,
    AnyUrl,
    computed_field
)

from typing_extensions import Self


from app.core.utils import parse_cors
from typing import Annotated ,Union , Literal


import warnings


from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    
    model_config=SettingsConfigDict(
        env_file=".env" , env_ignore_empty=True , extra="ignore"
    )
    
    PROJECT_NAME:str
    
    SECRET_KEY:str="badobadi_akh_lari_kadikadi"
    
    EMAIL_RESET_TOKEN_EXPIRE_HOURS:int=1
    
    API_V1_STR:str="api/v1"
    
    BACKENED_CORS:Annotated[list[AnyUrl]|str,BeforeValidator(parse_cors)]=[]
    
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    
    EMAILS_FROM_EMAIL:str | None=None
    EMAIL_FROM_NAME:str | None=None
    
    
    ENVIRNMENT:Literal["local","staging","production"]="local"
    
    WELCOME_MSG:str
    
    DOMAIN:str|None=None
    
    @computed_field
    @property
    def server_host(self)->str:
        if self.ENVIRNMENT=="local":
            return "http://localhost:3000"
        return f"https://{self.DOMAIN}"
    
    
    
    @model_validator(mode="after")
    def __setDefaultEmialsFrom(self)->Self:
        if self.EMAIL_FROM_NAME is None:
            warnings.warn(
                "Emails From name not set yet , Using Emials from Email instead"
            )
        
        self.EMAIL_FROM_NAME=self.PROJECT_NAME
        return self
    
    @computed_field
    @property
    def EmailEnabled(self)->bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)
    
    
    def _check_Default_Password_Mail(*,self,Variable_Name:str,Variable_Value:str):
        if Variable_Value=="Zendaya@actor@hollywood":
            message=(
                f"{Variable_Name}  ::  Default value ::{Variable_Value} is not secure , please change it to a secure Password , at least for Deployment"
            )
            if self.ENVIRNMENT=="local":
                warnings.warn(message)
            
            else: 
                raise ValueError(message)
    
    
    model_validator(mode="after")
    def _enforceNonDefaultSecrets(self)->Self:
        ... 
        self._check_Default_SecKeys(Variable_Name="SMTP Password",Variable_Value=self.SMTP_PASSWORD)   
        return self    

settings=Settings()    
            
    
    
    
    