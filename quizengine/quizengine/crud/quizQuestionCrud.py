from quizengine.models.quiz_models import (
    QuizQuestion,Quiz
)
from quizengine.core.loggerconfig import loggerconfigu
from fastapi import HTTPException , status
from sqlmodel import SQLModel , Session , select,and_,or_
from sqlalchemy.orm import selectinload
from quizengine.models.topic_models import Topic
from quizengine.models.answer_models import MCQOption
from quizengine.models.question_models import (
    QuestionBank , QuestionBankCreate
)


logger=loggerconfigu(__name__)


class QuizQuestionCrud():
    def createQuizQuestions(
          self,*,quizId:int, quizquestionData:QuestionBankCreate,db:Session
          ):
        
        print("jhbns")
        try:
            if not quizquestionData.is_verified :
                  raise HTTPException(
                      status_code=status.HTTP_400_BAD_REQUEST
                      ,detail="Question must be verified as True to be inserted in quiz"
                  )
                  
            if not db.get(Topic,quizquestionData.topic_id):
                raise   HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Topic not exist , that are belongs to it  "
                )
            quiz:Quiz=db.get(Quiz,quizId)
            
            if not quiz:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Quiz not found"
                )
            
            # print("Ola")
            
            # print(quizquestionData.option)           
            
            # if  quizquestionData.option:
            #      quizquestionData.option=[
            #          MCQOption.model_validate(option)
            #          for option in quizquestionData.option
            #      ]    
            # print(quizquestionData.option)           
            
            
            question:QuestionBank=QuestionBank.model_validate(quizquestionData)
            question.mcq_options=quizquestionData.options
            
            print(question.mcq_options)
            
            if not quizquestionData.topic_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="for which topic this question belongs to !? "
                )
                
            quizQuestion:QuizQuestion=QuizQuestion(
                quiz_id=quizId,question=question , topic_id=quizquestionData.topic_id
            )    
            
            db.add(quizQuestion)
            db.commit()
            db.refresh(quizQuestion)
            return quizQuestion
         
        except HTTPException as e:
            db.rollback()
            logger.error(f"create_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in creating Quiz Question",
            )
        except Exception as e:
            db.rollback()
            logger.error(f"create_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in creating Quiz Question",
            )   
            
            
    def removeQuizQuestion(self,*,quizId:int,quizQuestionId:int,db:Session):
         try:
             
            quiz:Quiz=db.get(Quiz,quizId)
            if not quiz:
                 raise HTTPException(
                     status_code=status.HTTP_404_NOT_FOUND,
                     detail="Not Found"
                 )
            
            quiz_question:QuizQuestion=db.exec(
                select(QuizQuestion)
                .where(
                    and_(
                        QuizQuestion.question_id==quizQuestionId,
                        QuizQuestion.quiz_id==quizId
                    )
                )
            ).one_or_none()
            # quiz_question:QuizQuestion=db.exec(
            #     select(QuizQuestion)
            #     .options(
            #         selectinload(QuizQuestion.quiz),
            #         selectinload(QuizQuestion.question)
            #     )
            #     .where(
            #         and_(
            #             QuizQuestion.question_id==quizQuestionId,
            #             QuizQuestion.quiz_id==quizId
            #         )
            #     )
            # ).one_or_none()
            
            print(quiz_question)
            
            if not quiz_question:
                raise HttpException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Quiz Question not found"
                )     
            
            
            db.delete(quiz_question)
            db.commit()
            return {"message": "Quiz Question deleted successfully!"}
         except HTTPException as e:
            db.rollback()
            logger.error(f"remove_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz Question not found"
            ) from e
         except Exception as e:
            db.rollback()
            logger.error(f"remove_quiz_question Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in deleting Quiz Question",
            ) from e

             
             
    
    
    
quezQuestion=QuizQuestionCrud()    
