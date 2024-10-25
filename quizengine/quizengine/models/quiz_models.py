from sqlmodel import SQLModel , Relationship,Field
from datetime import datetime 
from typing import List , Dict
from typing import Optional , Any , List , Union
from quizengine.models.linkmodels import QuizesTopics
from quizengine.models.base import BaseIdModel , QuizAttemptStatus,QuestionDifficultyEnum , QuizDifficultyEnum , QuestionTypeEnum 
from typing import TYPE_CHECKING
from quizengine.models.quiz_settings import QuizSetting
from quizengine.models.question_models import QuestionBankRead

if TYPE_CHECKING:
    from quizengine.models.question_models import QuestionBank
    # from quizengine.models.quiz_settings import QuizSetting
    

example_quiz_input = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    "course_id": 1,
}

example_quiz_input_create = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    # "course_id": 1,
    "add_topic_ids": [1],
}

example_quiz_input_update = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    # "course_id": 1,
    "add_topic_ids": [1, 2, 3],
    "remove_topic_ids": [4],
}

example_quiz_output = {
    "quiz_title": "TypeScript Quiz",
    "difficulty_level": "easy",
    "random_flag": True,
    # "course_id": 1,
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z",
}
    

    
class QuizBase(SQLModel):
    quiz_title:str=Field(max_length=150, index=True)
    difficulty_level:QuizDifficultyEnum=Field(default=QuizDifficultyEnum.easy) 
    random_flag:bool=Field(default=False)
    # total_points:int|None=Field(default=0)
    # course_id:int|None   
    
    class Config:
        json_schema_extra={"example":example_quiz_input}
        
        

class Quiz(BaseIdModel , QuizBase , table=True):
    topics:List["Topic"] =Relationship(back_populates="quizzes",link_model=QuizesTopics)       
    quiz_settings:List["QuizSetting"]=Relationship(
        back_populates="quiz", 
        sa_relationship_kwargs={
            "cascade":"all,delete-orphan",
            "lazy":"selectin"
        }
    )
    
    quizquestion:list["QuizQuestion"]=Relationship(
        back_populates="quiz",
        sa_relationship_kwargs={
            "cascade":"all,delete-orphan",
        }
        )
    
    





class QuizCreate(QuizBase):
    add_topic_ids:List[int]=[]   
    
    class Config:
        json_schema_extra={"example":example_quiz_input_create}
          
    

class QuizRead(QuizBase):
    id:int
    created_at:datetime    
    updated_at:datetime    
    

class QuizReadWithTopics(QuizBase):
    topics:list["Topic"]=[]
    

class QuizUpdate(SQLModel):
    quiz_title: str | None = None
    difficulty_level: QuizDifficultyEnum | None = None
    random_flag: bool | None = None
    # total_points: int | None = None
    # course_id: int | None = None
    
    add_topic_ids: List[int] = []
    remove_topic_ids: List[int] = []

    class Config:
        json_schema_extra = {"example": example_quiz_input_update}        


        
#  QuizQuestions   
example_quiz_question_input = {"quiz_id": 1, "question_id": 1, "topic_id": 1}



class  QuizQuestionBase(SQLModel):
    quiz_id:int|None=Field(
        foreign_key="quiz.id" , default=None,primary_key=True
    )
    question_id:int|None=Field(
        foreign_key="questionbank.id" , default=None,primary_key=True
    )
    topic_id:int|None=Field(
        foreign_key="topic.id" , default=None,primary_key=True
    )

    class Config:
        json_schema_extra={"example":example_quiz_question_input}       



class QuizQuestion(QuizQuestionBase,table=True):
    
    topic:"Topic"=Relationship(back_populates="quiz_question")
    question:"QuestionBank"=Relationship(back_populates="quiz_question")
    quiz:"Quiz"=Relationship(back_populates="quizquestion")
    
    
    
class QuizQuestionRead(QuizQuestionBase):
    ...
    
class QuizQuestionReadQuestionBank(QuizQuestionBase):
    question: QuestionBankRead
    

class QuizReadWithQuestionsAndTopics(QuizReadWithTopics):
    quiz_questions: list["QuizQuestionReadQuestionBank"] = []  