from fastapi import APIRouter
from app.api.V1.Routes import certification
from app.api.V1.Routes import edu
from app.api.V1.Routes import skill
from app.api.V1.Routes import profile

connect=APIRouter()

connect.include_router(certification.connect, prefix="/profile/certification", tags=["Certifications"])
connect.include_router(edu.connect, prefix="/profile/edu", tags=["Educations"])
connect.include_router(skill.connect, prefix="/profile/skills", tags=["Skills"])
connect.include_router(profile.router, prefix="/profile", tags=["Profile"])