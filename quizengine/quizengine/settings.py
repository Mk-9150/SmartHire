from quizengine.core.utils import parse_cors

from starlette.config import Config
from starlette.datastructures import Secret


try:
    config=Config(".env")
except :
    config=Config("")
    
PROJECT_NAME:str =config("PROJECT_NAME",cast=str)

print(PROJECT_NAME)

DESCRIPTION:str=config("DESCRIPTION",cast=str)
ENV:str=config("ENV", cast=str)
print(ENV)

DATABASE_URL:Secret=config("DATABASE_URL",cast=Secret)

BACKEND_CORS_ORIGINS_STR=config("BACKEND_CORS_ORIGINS",cast=str)     

BACKEND_CORS_ORIGINS :list[str] = parse_cors(BACKEND_CORS_ORIGINS_STR)

print(BACKEND_CORS_ORIGINS)

API_V1_STR:str="/api/v1"





