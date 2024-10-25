from quizengine.models.question_models import (
    QuestionBank,
    QuestionBankCreate,
    QuestionBankRead,
    QuestionBankUpdate,
)
from typing import Annotated , Optional , Union , Literal,Sequence

from fastapi import  HTTPException ,Depends,status,Query  , APIRouter,Path
from quizengine.core.loggerconfig import loggerconfigu
from quizengine.api.deps import DbDependency
from quizengine.crud.questionCrud import questionBnk

router = APIRouter()

logger=loggerconfigu(__name__)

router.post("/create")
def createQuestion(QuestionData:QuestionBankCreate , db:DbDependency):
    
    logger.info("%s.create_a_question: %s", __name__, QuestionData)
    try:
        return questionBnk.createQuestion(question=QuestionData, db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@router.get("/")
def readAllQuestions( *,
                    page:int=Query(default=0),
                    per_page:int=Query(default=10),
                    db:DbDependency ):
    
    logger.info("%s.get_all_questions", __name__)
    
    try:
        ...
        return questionBnk.readAllQuestion(page=page,perpage=perpage,db=db)    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
@router.get("/bytype")
def readQuestionByTypes(*,questionType:str=Query(default="single_select_mcq"),db:DbDependency):

    logger.info("%s.get_all_questions_by_type: %s", __name__, questionType)
    
    try :
          return questionBnk.readQuestionByType(questionType=questionType,db=db)       
         
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     
         
         
@router.get("/ques/{topicId}")
def getQuestionbByTopicID(topicId:Annotated[int,Path()],db:DbDependency):
    
    logger.info("%s.get_all_questions_by_topic: %s", __name__, topicId)
    
    try:
        ...
        return questionBnk.readQuestionBytopicID(topicId=topicId , db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

@router.get("/{questionid}")
def RedQuestionByID(*,questionid:int=Path(),db:DbDependency):
    
    logger.info("%s.get_question_by_id: %s", __name__, questionid)
    
    try:
        return questionBnk.readQuestionByiD(questionId=questionid,db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.patch("/update/{questionid}")
def updateQuestion(*,questionid:int=Path(),updateData:QuestionBankUpdate,db:DbDependency):
    ...
    
    logger.info("%s.update_question: %s", __name__, updateData)
    
    try:
        
        return questionBnk.updateQuestion(questionId=questionid,updateQuestion=updateData,db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

 


@router.delete("/{question_id}")
def call_delete_question(question_id: int, db: DbDependencyx):
    logger.info("%s.delete_question: %s", __name__, question_id)
    try:
        # return questionBnk.deleteQuestion(questionId=question_id,db=db)
        return questionBnk.deleteQuestion(questionId=question_id,db=db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        