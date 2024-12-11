from fastapi import FastAPI 
from fastapi.responses import RedirectResponse
from sqlmodel import SQLModel
from app.models import model
from app.core.db_settings import engine
from app.core.app_setting import setting
from contextlib import  asynccontextmanager
from app.api.V1.connect  import connect_router
import datetime
import pytz

def create_Table():
   SQLModel.metadata.create_all(engine)  


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Starting Application")
    # create_Table()
    yield
    print("Shutting down")
    
app = FastAPI(lifespan=lifespan)


# date=datetime.datetime.now(pytz.timezone('Australia/Sydney'))
# print(date.astimezone(pytz.utc))   # 2024-12-03 11:39:23.172730
# print(date) 

app.include_router(connect_router, prefix=f"{setting.API_V1_STR}", tags=["API"])

# alembic revision --autogenerate -m "Create a baseline migrations"
@app.get("/")
def pushToDocs()->RedirectResponse:
    return RedirectResponse(url="/docs")

