
from datetime import datetime

from sqlmodel import SQLModel , select , and_ , or_ , Session
from typing import Any , Annotated , Optional , Union
from fastapi import HTTPException,status
from  quizengine.models.quiz_settings import (
    QuizSetting ,
    QuizSettingCreaste,
    QuizSettingRead,
    QuizSettingUpdate
)




class QuizSetting():
    def createQuizSetting(self,*,settingData:QuizSettingCreaste,db:Session):
        
      try:
          
          if settingData:
              
              # check If quiz_Key is already used for the quiz , then raise the Error :
              CheckingForQuizKeyinUse=db.exec(
                  select(QuizSetting)
                  .where(and_(
                      QuizSetting.quiz_id == settingData.quiz_id,
                      QuizSetting.quiz_Key ==settingData.quiz_key                      
                  ))
              ).all()
              
              if len(CheckingForQuizKeyinUse) >=1:
                  raise HTTPException(
                      status_code=status.HTTP_400_BAD_REQUEST
                      ,detail="quiz Key already Used for Quiz "
                  )

              quizSetting=QuizSetting.model_validate(settingData)
              db.add(quizSetting)
              db.commit()
              db.refresh(quizSetting)
              return quizSetting
          
              
          
          
      except HTTPException as httpErr:
          db.rollback()
          raise httpErr
          ...    
      except Exception as e:
            db.rollback()
            logger.error(f"create_quiz_setting Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))   
          
      
    def GetAllQuizSettings(self,*,quizId:int,db:Session):
        
        try:
            quizSetting=db.exec(
                select(QuizSetting)
                .where(QuizSetting.quiz_id == quizId)
            ).all()

            if not quizSetting:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No Quiz Setting Found for the Quiz"
                )

            return quizSetting

        except HTTPException as httpErr:
            db.rollback()
            raise httpErr
        except Exception as e:
            db.rollback()
            logger.error(f"GetAllQuizSettings Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        
    def GetQuizSettingByID(self,*,settingId:int,db:Session):
        
        
        try:
            # Quizsetting:QuizSetting=db.exec(
            #     select(QuizSetting)
            #     .where(QuizSetting.id == settingId)
            # ).one()
            
            settings=db.get(QuizSetting,settingId)
            if settings is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No Quiz Setting Found for the Quiz"
                )
            return settings
            
            
           
        except Exception as e : 
            db.rollback()
            logger.error(f"get_quiz_setting_by_id Error: {e}")
            raise   HTTPException(status_code=400, detail=str(e))


    def UpdateQuizSettings(self,*,setting_id:int,settingsData:QuizSettingUpdate, db:Session):
        
        try:
            
            
            #first chk that quizkey is already used for quiz  or not if not then creste setting else error : quiz key already used  
            chiecking :list[QuizSetting]=db.exec(
                select(QuizSetting)
                .where(and_(
                    QuizSetting.quiz_id == setting_id,
                    QuizSetting.quiz_Key ==settingsData.quiz_key
                ))
                )
            
            if len(chiecking)>=1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Quiz Key already used for Quiz"
                )
                
            
            
            quizSetting=db.get(QuizSetting,setting_id)
            if not quizSetting:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No Quiz Setting Found for the Quiz"
                )
            
            updatedData=settingsData.model_dump(exclude_unset=True)
            
            quizSetting.sqlmodel_update(updatedData)
            db.add(quizSetting)
            db.commit()
            db.refresh(quizSetting)
            return quizSetting
        
                
           
        except Exception as e:
            db.rollback()
            logger.error(f"update_quiz_setting Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        
        
    def removeQuizSetting(self,*,setting_id:int,db:Session):
        
        try:
                    removedSetting=db.get(QuizSetting,setting_id)
                    if not removedSetting:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Quiz Setting Found for the Quiz"
                        )
                    
                    db.delete(removedSetting)
                    dv.commit()
                    return {"Message":"QuizSettign has been deleted successfully"}
        except Exception as e:
            db.rollback()
            logger.error(f"remove_quiz_setting Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))
                 
         
            
        # chking quizkey id Valid            
    def ValidateQuizKey(self,*,quizId:int, quizKey:str,db:Session):
        
        try:
            
            quizSetting:QuizSetting =db.exec(
                select(QuizSetting)
                .where(and_(
                    QuizSetting.quiz_id == quizId,
                    QuizSetting.quiz_Key == quizKey
                ))
            ).one_or_none()
            
            

            if not quizSetting:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No Quiz Setting Found for the Quiz"
                )
            
            if quizSetting.start_time and quizSetting.end_time:
                if (
                    not quizSetting.start_time
                    <= datetime.now()
                    < quizSetting.end_time
                    # <= quizSetting.end_time
                ):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Quiz is not active at the moment",
                    )
                    
            return quizSetting        
            
                    
        except HTTPException as httperr:
            db.rollback()
            logger.error(f"is_quiz_key_valid Error: {httperr}")
            raise httperr
        except Exception as e:
            db.rollback()
            logger.error(f"is_quiz_key_valid Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))        
        
quizSetting=QuizSetting()        