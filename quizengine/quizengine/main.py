from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from quizengine import settings
from sqlmodel import Session ,select
from quizengine.core.db_eng import engine
from quizengine.models.topic_models import Topic
from quizengine.core.loggerconfig import loggerconfigu
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from quizengine.api.v1 import api as v1_api

from fastapi.responses import RedirectResponse

from datetime import datetime

from quizengine.settings import BACKEND_CORS_ORIGINS
logger=loggerconfigu(__name__)


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("Starting up ...")
    allowedOrigin=[str(origin).strip("/")  for origin in BACKEND_CORS_ORIGINS ] 
    # print("allowed Origin",allowedOrigin)    
    yield
    logger.info("App shuting down")



def getServer():
     return [{"url": "http://localhost:8000", "description": "Development Server"}]


app=FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    servers=getServer(),
    lifespan=lifespan
    )

app.include_router(v1_api.apiRoute , prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def returnToDocs():
    return RedirectResponse(url="/docs")






          