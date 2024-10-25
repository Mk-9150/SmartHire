
# import secrets
# import warnings

from typing import Literal,Annotated
# from typing_extensions import Self
# from pydantic import (
#     model_validator,
#     BeforeValidator,
#     computed_field,
#     AnyUrl
# )

from pydantic_settings import (
    BaseSettings ,
    SettingsConfigDict
)


class Settings(BaseSettings):
    
    model_config  = SettingsConfigDict(
        env_file=".env",env_ignore_empty=True,extra="ignore"
    )
    API_V1_STR:str="/api/v1"
    # SECRET_KEY:str=secrets.token_urlsafe(32)
    # print('secret key :',SECRET_KEY)
    
    # ACCESS_TOEKN_EXPIRE_MINUTES:int = 60*24*1 #= 1 day
    
    # REFRESH_ACCESS_TOEKN_EXPIRE_MINUTES:int =60*24*8 #= 8 day
        
    DOMAIN:str="localhost:3000"
    
    # Environment: local, staging, production
    ENVIRONMENT:Literal["local","staging","production"]="local"
    
    # @computed_field
    # @property
    # def server_host(self)->str:
    # #    ...
    #    if self.ENVIRONMENT=="local":
    #        return "localhost:3000"
    #    return f"https://{self.DOMAIN}"
    
    # BACKEND_CORS_ORIGINS:Annotated[
    #     list[AnyUrl] | str , BeforeValidator(parse_cors)
    # ]=[]
    
    
    # @model_validator(mode="before")
    # @classmethod
    # def validate_cors_origins(cls,value):
    #     if isinstance(value,str):
    #         return [domen.strip() for domen in value.split(",")]
    #     return value
    
    PROJECT_NAME:str
    
    DATABASE_URL:str

    BOOTSTRAP_SERVER_KAFKA_URL:str

    KAFKA_TOPIC_NAME:str

    SCHEMA_REGISTRY_URL:str    
    
    KAFKA_TOPIC_NAME2:str
    
    # SMTP_TLS: bool = True
    # SMTP_SSL: bool = False
    # SMTP_PORT: int = 587
    # SMTP_HOST: str | None = None
    # SMTP_USER: str | None = None
    # SMTP_PASSWORD: str | None = None
    # # TODO: update type to EmailStr when sqlmodel supports it
    # EMAILS_FROM_EMAIL: str | None = None
    # EMAILS_FROM_NAME: str | None = None

    
    # @model_validator(mode="after")
    # def _setDefaultEmailsFrom(self)->Self:
    #     if self.EMAILS_FROM_NAME is None:
    #         warnings.warn(
    #             "EMAILS_FROM_NAME is not set, using EMAILS_FROM_EMAIL instead."
    #         )
    #         self.EMAILS_FROM_NAME=self.PROJECT_NAME
    #     return self
    
    
    #idk why used here
    # EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 1
    
    
    # @computed_field
    # @property
    # def emailsEnabled(self)->bool:
    #     return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)
    
    # ALGORITHMS:str
    
    
    # EMAIL_TEST_USER: str = "test@example.com"
    # # TODO: update type to EmailStr when sqlmodel supports it
    # FIRST_SUPERUSER: str
    # FIRST_SUPERUSER_PASSWORD: str
    # USERS_OPEN_REGISTRATION: bool = True
    
    # def _chkDefaultSecrets(self,varName:str,value:str)->Self:
    #     if value=="oyehoyebadobadi":
    #         message=(
    #              f'The value of {varName} is {value} "", '
    #             "for security, please change it, at least for deployments."
    #         )
    #         if self.ENVIRONMENT=="local":
    #             warnings.warn(message, stacklevel=1)
    #         else :
    #             raise ValueError(message)
            
            
    # @model_validator(mode="after")
    # def _enforceNonDefaultSecrets(self,)->Self:
    #     self._chkDefaultSecrets("SECRET_KEY",self.SECRET_KEY)            
    #     self._chkDefaultSecrets("FIRST_SUPERUSER_PASSWORD",self.FIRST_SUPERUSER_PASSWORD)
    #     return self
    
    
    
        
        

setting=Settings()
# print(setting.BACKEND_CORS_ORIGINS)
       
   
        
        



