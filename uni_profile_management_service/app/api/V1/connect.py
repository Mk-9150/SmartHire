from fastapi  import APIRouter
from app.api.V1.Routes import  profile

connect_router=APIRouter()

connect_router.include_router(profile.connect, prefix="/profile", tags=["Profile"])