from fastapi import FastAPI , HTTPException , Query , Depends
from typing import Optional , Union
# from fastapi.routing import APIRoute
from fastapi import APIRouter 
from quizengine.models.quiz_models import Quiz , QuizCreate , QuizUpdate 
from quizengine.api.deps import DbDependency
from    quizengine.core.loggerconfig import loggerconfigu
from quizengine.crud.quiz_crud import quizEngine
router=APIRouter()

logger= loggerconfigu(__name__)


@router.post("",)
def create_quiz(quiz:QuizCreate ,db:DbDependency):
    """
    Create a new Quiz

    Args:
        quiz (QuizCreate): Quiz to be created

    Returns:
        QuizReadWithQuizTopics: The created Quiz and QuizTopics Included

    Raises:
        HTTPException: Error in creating Quiz
    """
    
    logger.info(f"Creating Quiz : , {__name__},{ quiz} ")
    try:
        
        gen_quiz=quizEngine.createQuiz(quiz=quiz , db=db)
        # gen_quiz=quizEngine.Quizs(quiz_id=2,db=db)
        return gen_quiz
    
    except HTTPException as httpErr:
        logger.error(f"create_new_quiz Error: {http_err}")
        raise http_err
    
    except Exception as err:
        logger.error(f"create_new_quiz Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating Quiz"
        )
        
        

@router.get("/{quizId}")
def getQuizById(quizId:int , db:DbDependency):
    """
    Get_Quiz_by_ID

    Args:
        quizId (int): ID of the Quiz

    Returns:
        Quiz: The requested QuizwithTopicAndQuestions

    Raises:
        HTTPException: Error in getting Quiz
    """

    logger.info(f"Getting Quiz by ID: {quizId}, {__name__}")
    try:
        gen_quiz=quizEngine.GetQuizByIds(quiz_id=quizId, db=db)
        return gen_quiz

    except HTTPException as httpErr:
        logger.error(f"getQuizById Error: {httpErr}")
        raise httpErr

    except Exception as err:
        logger.error(f"getQuizById Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error in getting Quiz"
        )
    
    
    
@router.patch("/update/{quizId}")
def updateExistingQuiz(quizId:int,UpdatingData:QuizUpdate ,db:DbDependency):
        """
          Partially_Update_Existing_Quiz
        
        
        Args:
            quizId (int): ID of the Quiz to be updated
            UpdatingData (QuizUpdate): Updated Quiz Data
            db (DbDependency): Database Dependency
        
        Returns:
                Quiz: The updated Quiz
        
        Raises:
                    HTTPException: Error in updating Quiz
        """
        
        logger.info(f"Updating Quiz Data : , {__name__}, Quiz_id: {quizId}, Data : {UpdatingData}")
        try:
             
              UpdatedQuiz=quizEngine.UpdateQuiz(
                 quiz_id=quizId, updating_data=UpdatingData, db=db)
                
            
        
        except HTTPException : 
            logger.error("Eror")
            raise
            ...
        except Exception as e:
            logger.error(f"Quiz UpdATE Error :  {e}") 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error in updating Quiz"
            )
            
                

@router.delete("/{quidId}")
def DleteQuizById(quidId:int , db:DbDependency)  :
    
    if quidId:
        logger.info(f"Deleting existing Quiz: {__name__}, quiz_id: {quiz_id}")
        try:
            quiz_del=quizEngine.deleteQuiz(quiz_id=quidId,db=db)
            return quiz_del
        except HTTPException as http_err:
            logger.error(f"delete_existing_quiz Error: {http_err}")
            raise http_err
        except Exception as err:
            logger.error(f"delete_existing_quiz Error: {err}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )
    
    
          
        
        
        
    
            
        
   
   


