from fastapi import APIRouter 
from app.api.v1.Routes import like
from app.api.v1.Routes import coment


connect=APIRouter()


connect.include_router(like.router,prefix="/likes",tags=["likes"])
connect.include_router(coment.server , prefix="/comments" , tags=["comments"])