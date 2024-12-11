from fastapi import APIRouter
from app.api.V1.Routes  import relation
connect=APIRouter()


connect.include_router(relation.connect , prefix="/relations" , tags=["relations"])
