from fastapi import HTTPException , status , APIRouter  , Path
from  app.api.deps import Session_Depdnc
from typing import Annotated
from app.models import skills_models
# from app.crud import 
connect=APIRouter()

@connect.post("/skills/{teacher_id}")
def post_Skills(*,teacher_id=Path() ,data:skills_models.CreateSkill,  session:Session_Depdnc):
    ...
    try:
        return 
        ...
        
    except  Exception as e:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )  from e    
    