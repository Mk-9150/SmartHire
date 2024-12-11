from fastapi   import HTTPException , status, Path ,Query , APIRouter
from typing import Annotated , Optional
from app.models import model
from app.api.deps  import GET_TOKEN , Get_SESSION , GET_PRODUCER
from app.crud.jonposting  import uni_jobpost_crud
router=APIRouter()

@router.post("/create_job")
# def createPOst( uni_data:model.BasePost,  user:GET_TOKEN , producer:GET_PRODUCER , session:Get_SESSION):
def createPOst( post_data:model.BasePost,  user:GET_TOKEN  , session:Get_SESSION):
    ...
    try:
        ...
        return uni_jobpost_crud.createPost(uni_data=user , post_create=post_data , session=session)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{str(e.detail)}"
        ) from e.detail
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
        ) from e
        
@router.get("/get_all_post")        
def getAllPost(user:GET_TOKEN, session:Get_SESSION):
    ...
    try:
        ...
        return uni_jobpost_crud.getAllPost(uni_data=user, session=session)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{str(e.detail)}"
        ) from e.detail
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
        ) from e
        
        
@router.post("/appliedtojob/{jobpost_id}")
async def User_applying_toJob(*,jobpost_id:int=Path(),user_data:GET_TOKEN ,applier_data:model.JonApplicationBase ,producer:GET_PRODUCER,session:Get_SESSION):
    ...
    try:
        ...
        return  await  uni_jobpost_crud.jobAppliers(user=user_data, applierData=applier_data, producer=producer, jobpost_id=jobpost_id, session=session)
        
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{str(e.detail)}"
        ) from e.detail
    except  Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
        ) from e    
        
        
        #  getting Job infooo  
@router.get("/jobinfo/{jobpost_id}")
def infoJob(*,jobpost_id:int , session:Get_SESSION):
    ...
    try:
        ...
        return uni_jobpost_crud.getJobInfo(jobpost_id=jobpost_id, session=session)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{str(e.detail)}"
        ) from e.detail
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
        ) from e        
        

@router.get("/getapplier/{uni_id}/{jobpost_id}")
def getAppliers(*, uni_id:int=Path(), jobpost_id:int=Path(), session:Get_SESSION):
    ...
    try:
        ...
        return uni_jobpost_crud.getAppliers_specific_job(jobpost_id=jobpost_id,univeristy_id=uni_id,session=session)

    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{str(e.detail)}"
        ) from e.detail
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
        ) from e    
    
         