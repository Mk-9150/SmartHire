from fastapi import APIRouter , HTTPException , status 
from sqlmodel import Session ,select
from app.core.loggerConfig import loggeng
from app.api.deps import SessionEngine
from app.models.Institute_model import InstituteCreate , Institute
from app.crud.institute_crud import instituteCore
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from typing import Annotated



# from app.models.TeacherModel import Teacher,TeacherCreate


router=APIRouter()


logger=loggeng(__name__)

@router.post("/signup")
def createInstitute(session:SessionEngine, instituteCreate:InstituteCreate ):

    
    try:
      
      return  instituteCore.createInstitutes(institute_Create=instituteCreate,session=session)
        
    
    except HTTPException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )    from e 
        
        
        
        
    except Exception as e:
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR ,
            detail=f"Unexpercted Error {e} "
        )
        
        

@router.post("/login")        
def Login(formData:Annotated[OAuth2PasswordRequestForm,Depends()]):
    # ...
    try:
        
        
            
        ...
    except:
        ...    
    
        
    
     
    
    


    



