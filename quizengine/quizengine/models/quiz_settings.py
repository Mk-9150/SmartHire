from sqlmodel import SQLModel , Field , Relationship 
from datetime import datetime , timedelta
from typing import TYPE_CHECKING, Optional , Union
from quizengine.models.base import BaseIdModel
# from quizengine.models.quiz_models import Quiz

#  Response model
example_quiz_setting_input = {
    "quiz_id": 1,
    "instructions": "Read the questions carefully.",
    "time_limit": "PT50M",
    "start_time": "2023-02-26T14:56:46.277Z",
    "end_time": "2025-02-29T14:56:46.277Z",
    "quiz_key": "BAT_Q1TS278",
}

example_quiz_setting_output = {
    "quiz_id": 1,
    "instructions": "Read the questions carefully.",
    "time_limit": "P3D",
    "start_time": "2021-07-10T14:48:00.000Z",
    "end_time": "2021-07-10T14:48:00.000Z",
    "quiz_key": "BAT_Q1TS278",
    "created_at": "2021-07-10T14:48:00.000Z",
    "updated_at": "2021-07-10T14:48:00.000Z",
}


if TYPE_CHECKING : 
     from quizengine.models.quiz_models import Quiz


class  QuizSettingBase(SQLModel):
    quiz_id:int|None=Field(default=None,foreign_key="quiz.id")
    instructions:str|None=Field(default=None)
    time_limit: timedelta = Field()
    start_time: datetime
    end_time: datetime 
    quiz_key: str = Field(max_length=160)


class QuizSetting(BaseIdModel , QuizSettingBase , table=True):
    quiz:"Quiz"= Relationship(
        back_populates="quiz_settings",sa_relationship_kwargs={"lazy":"joined"}
        )
    
    
class QuizSettingCreaste(QuizSettingBase):
    pass
    class Config:
        json_schema_extra={"example":example_quiz_setting_input}    
        
        
class QuizSettingRead(QuizSettingBase):
    id:int
    created_at:datetime
    updated_at:datetime
    class Config:
        json_schema_extra={"example":example_quiz_setting_output}
        


class QuizSettingUpdate(SQLModel):
    instructions:str|None=Field(default=None)
    time_limit:timedelta|None=Field(default=None)
    start_time:datetime|None=Field(default=None)
    end_time:datetime|None=Field(default=None)
    quiz_id:int|None=None              
    quiz_key:str|None=None
    
    class Config:
        json_schema_extra={"example":example_quiz_setting_input}                           
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    