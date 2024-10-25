from fastapi import FastAPI,APIRouter 
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from app.core.loggerConfig import loggeng 
from app.api.v1 import connect_api  as API_V1
from starlette.middleware.cors import CORSMiddleware 
from app.core.settings import setting 


logger=loggeng(__name__) 


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("SatrtUp : triggered ")    
    yield


app:FastAPI=FastAPI(lifespan=lifespan)

# print(setting.BACKEND_CORS_ORIGINS)

app.include_router(API_V1.apiRoute , prefix=setting.API_V1_STR)


if setting.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip("/")  for origin in setting.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    
    
@app.get("/")
def root():
    return RedirectResponse(url="/docs")




    
    
    
        
    
    
