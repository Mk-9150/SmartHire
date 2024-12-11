from fastapi import HTTPException  , status , APIRouter  , UploadFile ,Body , Form
from app.models import certifications_model
from app.api.deps import Session_Depdnc
from app.crud.certificationCrud import certifi

from typing import Annotated

connect= APIRouter()

@connect.post("/certifications/{teacher_id}")
# async def post_Certifications(*,teacher_id:int ,c_text:certifications_model.CertificationText,image_file:UploadFile,  session:Session_Depdnc):
async def post_Certifications(*,teacher_id:int ,c_text:Annotated[str,Form()],image_file:UploadFile,  session:Session_Depdnc):
    
    """
        # - post Certifications when setting up the profile 
    """
    try:
        return await certifi.POst_certification(teacher_id=teacher_id,text=c_text, image_file=image_file, session=session)
        ...
    except  Exception as e:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )  from e

@connect.delete("/certifications/{certi_id}")
def delete_Certifications(*, certi_id:int, session:Session_Depdnc):
    ...
    try:
        return certifi.deleteCertifications(certification_id=certi_id, session=session)
        ...
    except  Exception as e:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )  from e