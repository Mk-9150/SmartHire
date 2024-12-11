from fastapi import FastAPI 
from sqlmodel import SQLModel
from  app.core.app_settings import setting
from app.core.db_setting import engine
from app.Models.test import test
import asyncio
from contextlib import asynccontextmanager
from app.api.v1 import connect as api_v1 
from app.crud.consumer  import L_consumer 
from app.core.db_setting import engine

def create_table():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app:FastAPI):
    # producer  and consumer is starting!
     
    # logger.info("Starting up ...")
    # allowedOrigin=[str(origin).strip("/")  for origin in BACKEND_CORS_ORIGINS ] 
    # create_table()
    # print("at life span")
    task_1=asyncio.create_task(L_consumer("liked","commented",setting.BOOTSTRAP_SERVER_KAFKA_URL,engine))
    # print("allowed Origin",allowedOrigin)    
    try:
        yield
    finally:
        task_1.cancel()
        await asyncio.gather(task_1, return_exceptions=True)    
    # logger.info("App shuting down")
    
app:FastAPI = FastAPI(
    lifespan=lifespan
)









#create table

app.include_router(api_v1.connect,prefix=setting.API_V1_STR)




@app.get("/")
def home():
    return f"{"Post service in progress"}, {setting.SCHEMA_REGISTRY_URL}"


