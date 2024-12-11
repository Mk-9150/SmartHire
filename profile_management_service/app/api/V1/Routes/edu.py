from fastapi import HTTPException , status , APIRouter
from app.models import education_model
from app.api.deps import Session_Depdnc
from app.crud.educationCrud import  edu

connect=APIRouter()


@connect.post("/education/{teacher_id}")
def post_Education(*,teacher_id:int ,data:education_model.CreateEducation,  session:Session_Depdnc):
    ...
    try:
        return edu.post_education(teacher_id=teacher_id,education=data,session=session)
    except  Exception as e:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )  from e