from quizengine.models.quiz_models import (
    QuizQuestion,Quiz
)
from quizengine.core.loggerconfig import loggerconfigu
from fastapi import APIRouter , HTTPException , status , Query ,Path

from quizengine.api.deps import DbDependency
from quizengine.models.question_models import QuestionBank,QuestionBankCreate
from quizengine.crud.quizQuestionCrud import quezQuestion


router=APIRouter()

logger=loggerconfigu(__name__)


@router.post("/{quizId}")
def CreateQuizQuestion(*,quizId:int=Path(),questionData:QuestionBankCreate ,db:DbDependency):
    
    logger.info("%s Creating the QuizQuestionLink   %s", __name__ , f"QuizId :{quizId} , QuestionData :{questionData}"  )
   
    try:
        
        print("ok")
               
        return quezQuestion.createQuizQuestions(quizId=quizId,quizquestionData=questionData,db=db)

    except HTTPException  as Http_Err:
        logger.error(f"create_new_quiz_question Error: {Http_Err}")
        raise Http_Err
    except Exception as e:
        logger.error(f"create_new_quiz_question Error: {err}")
        raise e


@router.delete("/{quiz_id}/quiz-question/{quiz_question_id}")
def callRemoveQuizQuestion(
    quiz_id: int, quiz_question_id: int, db: DbDependency
):

    logger.info(f"Removing existing Quiz Question: {__name__}")

    try:
     return quezQuestion.removeQuizQuestion(
            quizId=quiz_id, quizQuestionId=quiz_question_id, db=db
        )
    except HTTPException as http_err:
        logger.error(f"remove_quiz_question Error: {http_err}")
        raise http_err
    except Exception as err:
        logger.error(f"remove_quiz_question Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found"
        )


