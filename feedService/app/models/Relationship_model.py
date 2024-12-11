from sqlmodel import SQLModel , Field  , Relationship , Column
from typing import Annotated ,List ,  Optional , Any 
from sqlalchemy.dialects.postgresql import JSON 

import datetime


class Base():
    ...
    
class User(SQLModel, table=True):
    id:Annotated[int,Field(primary_key=True, default=None)]
    Actualuser_id:Annotated[int,Field(index=True)]
    username:Annotated[str,Field(unique=True, index=True)]
    haveRelation:Optional["UserRelationship"]=Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade":"all, delete-orphan"
        })
    haveFeed:Optional["Userfeed"]=Relationship(
        back_populates="userr",
        sa_relationship_kwargs={
            "cascade":"all, delete-orphan"
        })
    isapplier:Optional["UserJOBPost"]=Relationship(
        back_populates="appliedjobs",
        sa_relationship_kwargs={
            "cascade":"all, delete-orphan"
        })
        

# class Userfeed(SQLModel , table=True):
#     ...
#     id:Annotated[int,Field(primary_key=True, default=None)]
#     user_id:Annotated[str,Field(default=None, index=True, foreign_key="user.id")]
#     feed: Annotated[List[int], Field(sa_column=JSON, default_factory=list)]     
#     userr:"User" = Relationship(
#         back_populates="haveFeed",
#         sa_relationship_kwargs={
#             "cascade": "all, delete-orphan"
#         }
#         )        
    
    
class Userfeed(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True, default=None)]
    user_id: Annotated[int, Field(default=None, index=True, foreign_key="user.id")]
    feed: Annotated[List[int], Field(sa_column= Column(JSON), default_factory=list)]  # Correct JSON usage

    userr: Optional["User"] = Relationship(
        back_populates="haveFeed",
        sa_relationship_kwargs={
            "single_parent":True,
            "cascade": "all, delete-orphan"
        }
    )
    
class UserJOBPost(SQLModel , Table=True):
    id:Annotated[int,Field(primary_key=True, default=None)]
    user_id:Annotated[int,Field(default=None, index=True, foreign_key="user.id")]
    # post:Annotated[List[int],Field(sa_column=Column(JSON), default_factory=list)]
    
    #  in josposting service , table  jobapplication  has id(pk)  and jobid(fk)  these 2 id are here here in a tuple 
    appliedTo_id:Annotated[List[tuple[int,int]],Field(sa_column=Column(JSON), default_factory=list)]
    appliedjobs:Optional["User"] = Relationship(
        back_populates="isapplier",
        sa_relationship_kwargs={
            "single_parent":True,
            "cascade": "all, delete-orphan"
        }    )


        
    
class UserRelationship(SQLModel , table=True):
    id:Annotated[int,Field(primary_key=True , default=None)] 
    user_id:Annotated[int,Field(default=None, index=True , foreign_key="user.id")]    #  it is user primary key vali id   not user_id in User
    followed_by:Annotated[Optional[list[tuple[int,str]]] ,Field(sa_column=Column(JSON)  ,default_factory=list)]       
    following:Annotated[Optional[list[tuple[int,str]]] ,Field(sa_column=Column(JSON), default_factory=list)]
    follow_back:Annotated[Optional[list[tuple[int,str]]] ,Field(sa_column=Column(JSON), default_factory=list)]
    
    user:Optional["User"] = Relationship(
        
        back_populates="haveRelation",
        sa_relationship_kwargs={
            "single_parent":True,
            "cascade": "all, delete-orphan"
        }
        ) 
    