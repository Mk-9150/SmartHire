from fastapi import APIRouter
from app.api.v1.Routes import emial_service 


connect=APIRouter()


connect.include_router(emial_service.router )