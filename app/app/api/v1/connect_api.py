
from fastapi import APIRouter 
from app.api.v1.Routes import institue


apiRoute=APIRouter()

apiRoute.include_router(institue.router , prefix="/institute",tags=["institute"])
