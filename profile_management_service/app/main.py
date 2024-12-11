from fastapi import FastAPI 
from fastapi.responses import RedirectResponse
from sqlmodel import SQLModel
from app.models.teacher_model import Teacher
from app.models.education_model import Education
from app.models.skills_models import Skill
from app.models.certifications_model import Certification
from sqlalchemy import Engine
from app.core.app_setting import setting
from app.core.log_module import loggerconfigu
from contextlib import asynccontextmanager
from app.core.db_setting import engine
from app.api.V1 import connect as connect_router


log=loggerconfigu(__name__)



def create_tables(engine:Engine):
    ...
    log.info("creating tables")
    # SQLModel.metadata.create_all(engine)
    


@asynccontextmanager
async def lifespan(app:FastAPI):
    log.info("starting up")
    create_tables(engine)
    yield



app :FastAPI =FastAPI(lifespan=lifespan)


# arrey=[]

# arr2=[1,2,3]

# arrey.append(arr2)

# print(arrey)

app.include_router(connect_router.connect,prefix=f"{setting.API_V1_STR}")

@app.get("/")
# def pushToDocs()->RedirectResponse:
def pushToDocs():
    return "kdmnfk"
    # return RedirectResponse("/docs")