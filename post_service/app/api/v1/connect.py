from fastapi import APIRouter 

from app.api.v1.Routes import post


connect=APIRouter()


connect.include_router(post.router,prefix="/posts",tags=["posts"])