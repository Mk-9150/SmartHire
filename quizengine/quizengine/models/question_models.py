from sqlmodel import SQLModel , Field , Relationship
from typing import Optional , Union , TYPE_CHECKING

from quizengine.models.base import BaseIdModel , QuestionDifficultyEnum, QuestionTypeEnum
from quizengine.models.answer_models import MCQOption


if TYPE_CHECKING :
    from quizengine.models.quiz_models import QuizQuestion
    from quizengine.models.topic_models import Topic
        
    
# ------------------------------------------------
# QuestionBank Models
# ------------------------------------------------
example_input_question_bank = {
    "topic_id": 1,
    "question_text": "What is a common cause of syntax errors in TypeScript?",
    "is_verified": True,
    "points": 1,
    "difficulty": "easy",
    "question_type": "single_select_mcq",
}

example_output_question_bank = {
    "id": 1,
    "question_text": "What is a common cause of syntax errors in TypeScript?",
    "is_verified": True,
    "points": 1,
    "difficulty": "easy",
    "topic_id": 1,
    "question_type": "single_select_mcq",
    "options": [
        {
            "is_correct": True,
            "option_text": "Missing semicolons at the end of statements",
        },
        {"is_correct": False, "option_text": "Missing types in function parameters"},
    ]
}

example_input_with_options_question_bank = {
    "question_text": "What is a common cause of syntax errors in Dockefile?",
    "is_verified": True,
    "points": 1,
    "difficulty": "easy",
    "topic_id": 1,
    "question_type": "single_select_mcq",
    "options": [
        {
            "is_correct": True,
            "option_text": "Missing BaseImage at the start",
        },
        {"is_correct": False, "option_text": "Add COPY "},
    ]
}   

 
 


class QuestionBase(SQLModel):
    question_text: str
    is_verified: bool=False
    points: int=Field(default=0)
    topic_id:int|None=Field(foreign_key="topic.id")
    difficulty: QuestionDifficultyEnum=Field(default=QuestionDifficultyEnum.easy)
    question_type: QuestionTypeEnum =Field(default=QuestionTypeEnum.single_select_mcq)
    class Config:
        json_schema_extra={"example":example_input_question_bank}


class QuestionBank(BaseIdModel , QuestionBase ,table=True):
    topic:"Topic"=Relationship(back_populates="questions")
    mcq_options:list["MCQOption"]=Relationship(
        back_populates="question",
        # sa_relationship_kwargs={
        #      "cascade":"all,delete-orphan",
        #     "lazy":"selectin"
        #     }
    )
    
    quiz_question:list["QuizQuestion"]=Relationship(
        back_populates="question",
        sa_relationship_kwargs={
            "cascade":"all,delete-orphan",            
        }
    )

    
    
    

    

    
 
class QuestionBankCreate(QuestionBase):
    options:list["MCQOption"]=[]

    class Config:
        json_schema_extra = {"example": example_input_with_options_question_bank}

    
    
    
class QuestionBankRead(QuestionBase):
    id:int
    options:list["MCQOption"]=[]
    class Config:
        json_schema_extra={"example":example_output_question_bank}
    
        
class QuestionBankUpdate(SQLModel):
    question_text: str | None = None
    is_verified: bool | None = None
    points: int | None = None
    difficulty: QuestionDifficultyEnum | None = None
    topic_id: int | None = None