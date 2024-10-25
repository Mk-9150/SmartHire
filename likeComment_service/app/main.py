# from aiokafka import l
from fastapi import FastAPI
from fastapi.responses import  Response  ,RedirectResponse,PlainTextResponse
from sqlmodel import SQLModel
from app.models import comment_model
from app.models import like_mode
from app.core.app_setting import setting
from app.core.db_setting import engine
from app.core.logger import Logger_Config
from contextlib import asynccontextmanager
from app.api.v1.connect import connect

logger=Logger_Config(__name__)

print(engine)

# def create_table():
#     # SQLModel.metadata.create_all(engine)
#     SQLModel.metadata.create_all(engine)
    

def create_table():
    SQLModel.metadata.create_all(engine)


create_table()

@asynccontextmanager
async def lifespan(app:FastAPI):
    # logger.info("Starting up ...")
    # allowedOrigin=[str(origin).strip("/")  for origin in BACKEND_CORS_ORIGINS ] 
    # create_table()
    # print("allowed Origin",allowedOrigin)    
    yield
    # logger.info("App shuting down")

server=FastAPI(
    
    # logger.info("table creating started")
    lifespan=lifespan
    
)

server.include_router(connect,prefix=f"{setting.API_V1_STR}")





# @server.get("/")
# def hello():
#     return "ok"
#     # return PlainTextResponse(content="Hello World", status_code=200)

@server.get("/")
def root()->Response:
    return RedirectResponse(url="/docs", status_code=302)

