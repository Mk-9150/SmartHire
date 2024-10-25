from sqlmodel import Field , Relationship , SQLModel
from typing import TYPE_CHECKING , Optional , Union
from datetime import datetime
from pydantic import EmailStr , validator
from quizengine.models.base import BaseIdModel

if TYPE_CHECKING :
    # from quizengine.models.quiz_models import Quiz
    from quizengine.models.question_models import QuestionBank
    

example_input_mcq_option = {
    "option_text": "Missing semicolons at the end of statements",
    "is_correct": True,
    "question_id": 1,
}

example_output_mcq_option = {
    "id": 1,
    "option_text": "Missing semicolons at the end of statements",
    "is_correct": True,
    "question_id": 1,
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z",
}



class MCQOptionBase(SQLModel):
    option_text:str=Field(max_length=140, default=None)
    is_correct:bool =False
    question_id:int|None=Field(foreign_key="questionbank.id",default=None)
    class Config:
        json_schema_extra={"example":example_input_mcq_option}    
        
class MCQOption(BaseIdModel , MCQOptionBase,table=True):
    question:Optional["QuestionBank"]=Relationship(
        back_populates="mcq_options",
        sa_relationship_kwargs={
            "lazy":"joined"
        }        
    )
    
    
class MCQOptionCreate(MCQOptionBase):
    ...
    
    
class MCQOptionRead(MCQOptionBase):
    id: int
    created_at: datetime
    updated_at: datetime


class MCQOptionUpdate(SQLModel):
    option_text: str | None = None
    is_correct: bool | None = None
    question_id: int | None = None
        
        