
from sqlmodel import SQLModel , Session , select
from quizengine.models.question_models import (
    QuestionBank,
    QuestionBankCreate,
    QuestionBankRead,
    QuestionBankUpdate,
)

from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from quizengine.models.answer_models import MCQOption , MCQOptionCreate 
from fastapi import  HTTPException ,status  
from quizengine.core.loggerconfig import loggerconfigu

logger=loggerconfigu(__name__)


class QuestionBanks():
    def createQuestion(self,*,question:QuestionBankCreate,db:Session):
        try:
           ...
           if question.option:
               question.option=[
                   MCQOption.model_validate(option)
                   for option in question.option
               ]
               
            
           db_question=QuestionBank.model_validate(question)
           
           db.add(db_question)
           db.commit()
           db.refresh(db_question)
        except IntegrityError as e:
            db.rollback()
            logger.error(
                f"Add Question :  An constraints voilation or integroty issue occured  :{e}"
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Add Question :  An constraints voilation or integroty issue occured  :{e}",
            ) from e
            
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(
                f"Add Question :  An database   issue occured while adding to the database it may be connection erorr or some else   :{e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database issue "
            )    from e
        
        except Exception as e:
            db.rollback()
            logger.error(f"ADD_Question: An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")
            
              
               
    def readAllQuestion(self,*,offset:int,limit:int,db:Session):
        
        try:            
            
            questions=db.exec(select(QuestionBank).offset(offset).limit(limit)).all()
            if not questions:
                raise ValueError("Question nOT Found")
            
            return questions
        except ValueError as e:
            logger.error(f"READ_Questions: No questions found: {e}")
            db.rollback()
            raise HTTPException(status_code=404, detail="No questions found")
        except SQLAlchemyError as e:
            logger.error(
                f"READ_Questions: A database error occurred while reading the Questions: {e}"
            )
            db.rollback()
            raise HTTPException(status_code=500, detail="Database operation failed.")
        except Exception as e:
            logger.error(f"READ_Questions: An unexpected error occurred: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")           
        


    def readQuestionByType(slef,*,questionType:str,db:Session):
        try:
            questions=db.exec(select(QuestionBank).where(QuestionBank.question_type==questionType)).all()
            if not questions:
                raise ValueError("Question nOT Found")

            return questions
        except ValueError as e:
            logger.error(f"READ_Questions: No questions found: {e}")
            db.rollback()
            raise HTTPException(status_code=404, detail="No questions found")
        except SQLAlchemyError as e:
            logger.error(
                f"READ_Questions: A database error occurred while reading the Questions: {e}"
            )
            db.rollback()
            raise HTTPException(status_code=500, detail="Database operation failed.")
        except Exception as e:
            db.rollback()
            logger.error(f"READ_Questions: An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")
        
    
    def readQuestionByiD(self,*,questionId:int,db:Session):
        try:
            question=db.exec(select(QuestionBank).where(QuestionBank.id==questionId)).first()
            if not question:
                raise ValueError("Question nOT Found")

            return question   
        except ValueError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            ) from e
        except Exception as e:
            db.rollback()
            raise Exception("An unexpected error occurred.") from e
    def updateQuestion(self,*,questionId:int,updateQuestion:QuestionBankUpdate , db:Session):
          try: 
              
              question:QuestionBank=db.get(QuestionBank,questionId)
              if not question:
                  raise ValueError("Question not found")
              
              questionDict=updateQuestion.model_dump(exclude_unset=True)
              question.sqlmodel_update(questionDict)
              db.add(question)
              db.commit()
              db.refresh(question)
              return question
          except ValueError:
            db.rollback()
            logger.error("UPDATE_Question: Question not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
          except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"UPDATE_Question: Error updating question: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            ) from e
          except Exception as e:
            db.rollback()
            logger.error(f"UPDATE_Question: Error updating question: {str(e)}")
            raise Exception("Error updating question")
        
        
    def deleteQuestion(self,*,questionId:int,db:Session):
        
        try:
            ...
            
            question:QuestionBank=db.get(QuestionBank,questionId)
            if not question :
                raise ValueError("no Question Found ")
            
            db.delete(question)
            db.commit()
            return {"message":"Question with its McqS has been deleted"}
            
            
        except ValueError as e:
            db.rollback()
            logger.info(
                "%sDeleting the Question:  No Question Found   %s " ,str(e)
                )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND ,
                detail="No question found"
            )
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Deleting _Question: Error deleting question: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed.",
            ) from e
        except Exception as e:
            db.rollback()
            logger.error(f"Deleting_Question: Error Deleting question: {str(e)}")
            raise Exception("Error updating question") from e 
        
    def readQuestionBytopicID(self,*,topicId:int,db:Session):
        
        
        try:
            questionsbyTopic:list[QuestionBank]=db.exec(
                                                    select(QuestionBank)
                                                    .where(QuestionBank.topic_id==topicId)
                                                    ).all()
            
            if not questionsbyTopic:
                raise ValueError("questions not found")
            
            return questionsbyTopic
        except ValueError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No questions found"
            ) from e
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            ) from e 
    
    
    
        
   

questionBnk=QuestionBanks()        