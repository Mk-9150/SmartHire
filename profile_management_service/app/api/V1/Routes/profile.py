from fastapi import APIRouter , Depends, HTTPException, status
# from sqlmodel import Session
from app.api.deps import get_TokenData
from app.api.deps import Session_Depdnc
from app.crud.profileCrud import techer
from app.models.teacher_model import TeachrCreate , UpdateModel
router=APIRouter()




@router.get("/profile/me")
def get_user_profile(tokenData:get_TokenData,session:Session_Depdnc):
    ...
    try:
        ...
        return     techer.get_profile(user=tokenData.username,session=session)
    except HTTPException as e:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )  from e
            


@router.post("/profile/setup")
def Create_Profile(tokenData:get_TokenData, teacher:TeachrCreate , session:Session_Depdnc):
    ...
    try:
        ...
        return techer.create_profile( username=tokenData.username,teacher=teacher,session=session)
    except HTTPException as e:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )  from e    
        


@router.patch("/id")
def Updates_Profile(data:UpdateModel , session:Session_Depdnc):
    ...        
    try:
        ...  
    except   Exception as e:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )  from e   