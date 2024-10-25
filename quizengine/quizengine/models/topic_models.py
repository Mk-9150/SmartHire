from typing import TYPE_CHECKING,Optional,Union
from quizengine.models.base import BaseIdModel
from datetime import datetime
from sqlmodel import SQLModel ,Field  ,Relationship
from quizengine.models.linkmodels import QuizesTopics
from quizengine.models.question_models import QuestionBank
if TYPE_CHECKING :
    # from quizengine.models.quiz_models import Quiz
    from quizengine.models.quiz_models import Quiz,QuizQuestion
    
    
example_topic_input = {
    "parent_id": None,  # "None" for root topic
    "title": "Python",
    # "course_id": 1,
    "description": "Python programming language",
}

example_topic_input_with_content = {
    "title": "OOP Paradigm",
    "description": "Learn OOPS in Python12",
    # "course_id": 1,
    "parent_id": 1,  # This is Optional for Subtopics
    "contents": [
        {
            "content_text": "OOP is a programming paradigm based on classes and objects rather."
        },
        {
            "content_text": "OOP Pillars: Encapsulation, Inheritance and Polymorphism, and Abstraction."
        },
    ],
}


class TopicBase(SQLModel):
    title:str=Field(index=True)
    description:str
    parent_id:int|None=Field(
        default=None,
        foreign_key="topic.id"
    )
    
    class Config:
         json_schema_extra=example_topic_input
         

class Topic(BaseIdModel , TopicBase , table=True):
    children_topics:list["Topic"]=Relationship(back_populates="parent_topic")   
    parent_topic:Optional["Topic"]=Relationship(
        back_populates="children_topics",
        sa_relationship_kwargs=dict(
            remote_side="Topic.id",
            lazy="selectin"
        )
        )
    
    quiz_question:list["QuizQuestion"]=Relationship(
        back_populates="topic",
        sa_relationship_kwargs={
            "cascade":"all,delete,delete-orphan",
        }
        )
    
    quizzes:list["Quiz"]=Relationship(back_populates="topics",link_model=QuizesTopics)
    
    questions:list["QuestionBank"]=Relationship(
        back_populates="topic",
        sa_relationship_kwargs={
            "cascade":"all,delete,delete-orphan",
            "lazy":"select"
        })
    
        


class TopicCreate(TopicBase):
              ...
              
              
class TopicResponse(TopicBase):
    id:int
    # parent_id:int|None=None
    created_at:datetime
    updated_at:datetime       
    
    
class TopicUpadate(SQLModel):
    title:str|None=None
    description:str|None=None
    # parent_id:int|None=None
    
    
class TopicResponseWithQueations(TopicResponse):
        Questions:list["QuestionBank"]=[]
        
        
class PaginatedTopicRead(SQLModel):
    
    count:int
    nextp:Union[str,None]=None
    previous: Union[str, None] = None
    results: list[TopicResponse]=[]
    
    
    ...        