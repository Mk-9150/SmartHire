from fastapi import APIRouter , HTTPException , Depends , status

from quizengine.api.deps import DbDependency 

from quizengine.models.quiz_settings import (
    QuizSetting ,
    QuizSettingCreaste,
    QuizSettingRead ,
    QuizSettingUpdate
  )
from quizengine.core.loggerconfig import loggerconfigu
from quizengine.crud.quizSettingCrud import quizSetting

logger =loggerconfigu(__name__)

router = APIRouter()

@router.post("/create")
def CreateNewQuizSetting( settingCreate:QuizSettingCreaste  ,db:DbDependency):
    """
    Create a new QuizSetting
    """
    
    logger.info(f"Creating new Quiz Setting : {__name__}  ,  quizSetting : {settingCreate}") 
    
    try:
         return quizSetting.createQuizSetting(settingData=settingCreate,db=db)    
        
    except HTTPException as httpErr :
        logger.error(f"Createing New Quiz Setting Error : {httpErr}  ")
        raise
    except Exception as e:
        logger.error(f"Createing New Quiz Setting Error : {httpErr}  ")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error in Creating Quiz Settings"
        )
                
    
    
#Get all Quiz Settings     
@router.get("/{quizid}",)
def GetAllQuizSettings(quizid:int ,db:DbDependency):
    """
      
      Get All Quiz Setting 
      
    """
    try:
         return quizSetting.GetAllQuizSettings(quizId=quizid,db=db)
    except Exception as err:
        logger.error(f"get_all_quiz_settings_endpoint Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error in fetching QuizSettings",
        )
        

@router.get("/{settingId}")
def GetQuizSettingByID(settingId:int ,  db:DbDependency):
    
    
    try:
        return quizSetting.GetQuizSettingByID(settingId=settingId,db=db)
    except Exception as e :
        logger.error(f"get_quiz_setting_by_id_endpoint Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QuizSetting not found"
        )
        

@router.patch("/{settingid}")
def updateQuizSetting(settingid:int , UpdateSettingData:QuizSettingUpdate, db:DbDependency):
    
    try:
           
        quizSetting:QuizSetting=quizSetting.UpdateQuizSettings(setting_id=settingid,settingsData=UpdateSettingData, db=db)
        
        ...
    except Exception as e:    
        logger.error(f"update_quiz_setting_endpoint Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error in updating QuizSetting",
        )
        
        
        
    except Exception as e :
        logger.error(f"")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,detail=str(e))    
            
        
@router.delete("/{settingId}")
def removeSettingById(settingId:int):
    try:
        
        return quizSetting.removeQuizSetting(setting_id=settingId,db=db)
    except Exception as err:
        logger.error(f"remove_quiz_setting_endpoint Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QuizSetting not found"
        )
        