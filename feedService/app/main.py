from fastapi import FastAPI 
import pytz
from fastapi.responses import RedirectResponse
from contextlib import  asynccontextmanager
from app.api.V1 import connect as routerr
from sqlmodel import SQLModel
from app.models import Relationship_model
from app.core.app_setting import setting
from app.core.db_settings import engine
from app.crud.consumer import FeedConsumer
from app.models import time_timezone_model
from app.crud.consumerPost import PostConsumer
from app.crud.consumerJobPost import JobPostConsumer
import asyncio
import datetime

def create_table():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Starting Application")
    print("Creating tables")
   
    
    task_1=asyncio.create_task(FeedConsumer(setting.KAFKA_TOPIC_Account_Created , setting.BOOTSTRAP_SERVER_KAFKA_URL , engine))
    task_2=asyncio.create_task(PostConsumer(setting.KAFKA_TOPIC_POST_CREATED,setting.BOOTSTRAP_SERVER_KAFKA_URL , engine))
    task_3=asyncio.create_task(JobPostConsumer(setting.Topic_Applier,setting.BOOTSTRAP_SERVER_KAFKA_URL , engine))
    try:
        ...
        yield
    finally:
        task_1.cancel()
        task_2.cancel()
        task_3.cancel()
        await asyncio.gather(task_1, task_2, task_3, return_exceptions=True)    
    

app = FastAPI(lifespan=lifespan)

# print("hello ======================?")
# timezone = pytz.timezone('Asia/Karachi')
# print(timezone)

# timezonemodle=time_timezone_model.LocalTimePlus_imeTimeZone(timezone="Asia/Karachi",localTime=datetime.datetime.now(pytz.timezone("Asia/Karachi")))
# print("okokko")
# print(timezonemodle)

app.include_router(routerr.connect, prefix=f"{setting.API_V1_STR}")

# print(datetime.datetime.now(timezone))



# curr=datetime.datetime.now()
# curr=datetime.datetime.now(pytz.timezone("Asia/Karachi"))
# print(curr.astimezone(pytz.utc))  #  2024-12-02 19:45:50.721532+00:00
                                  #    2024-12-03 01:04:36.369389+05:00
                                #      24-12-02 20:06:35.333211+00:00
                                    #  2024-12-03 04:33:38.010297+00:00
# print(datetime.datetime.now(pytz.utc))
# print(datetime.datetime.now(datetime.timezone.utc))
# print(curr.astimezone(pytz.utc))

# curr=curr.astimezone(pytz.timezone("Asia/Karachi"))
# isoformet=curr.isoformat()
# curr=curr.astimezone(pytz.timezone("UTC"))
# print(isoformet)
# aware=curr.replace(tzinfo=datetime.timezone.utc)
# print(aware)

@app.get("/")
def pushToDocs()->RedirectResponse:
    return RedirectResponse(url="/docs")

