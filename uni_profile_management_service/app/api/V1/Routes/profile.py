from sqlmodel  import Session 
from fastapi import HTTPException , status ,APIRouter  , Path 
from app.models import model
from app.crud.uniCrud import uniprofilecrud
from typing import Annotated
from app.api.deps  import Get_SESSION



connect=APIRouter()

@connect.post("/create_uni")
def create_uni(uni:model.Unicreate,session:Get_SESSION):
    try:
       ...
    #    return uni
       return uniprofilecrud.CreateUni(uni_create=uni, session=session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   from e

@connect.patch("/update_uni/{uni_id}")
def updateUniversityProfile(uni_id:Annotated[int,Path()], uni:model.UpdateModel, session:Get_SESSION):
    try:
        return uniprofilecrud.updateUni(uni_id=uni_id, uni_update=uni, session=session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   from e