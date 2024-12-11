from sqlmodel import SQLModel, Field , Relationship
from typing import Optional  , Annotated , List
from app.models.base  import BaseDateTime
from sqlmodel  import Column
from sqlalchemy.dialects.postgresql import JSON
from dataclasses import field
from dataclasses import field

class Unicreate(SQLModel):
    # username:Optional[str]=Field(default_factory=lambda : "")
    username:str
    emails:Optional[str]=None	          
    contact_number:int
    website:Annotated[str|None, Field(default_factory=lambda : "")]	
    description	:Optional[str]=Field(default_factory=lambda : "")	
    departments	:list[str] = Field(sa_column=Column(JSON) , default_factory=list) 
    logo_url  :Annotated[Optional[str],Field(default_factory=lambda : "")]	
    verified :bool = Field(default=False)
    linkedin_url:Optional[str]=Field(default_factory=lambda : "")    
    facebook_url:Optional[str]=Field(default_factory=lambda : "")    
    instagram_url:Optional[str]=Field(default_factory=lambda : "")    
    


class UpdateModel(SQLModel):
    ...
    emails:Optional[str]=None	          
    contact_number:int
    website:Annotated[str|None, Field(default_factory=lambda : "")]	
    description	:Optional[str]=Field(default_factory=lambda : "")	
    departments	:list[str] = Field(sa_column=Column(JSON) , default_factory=list) 
    logo_url  :Annotated[Optional[str],Field(default_factory=lambda : "")]
    linkedin_url:Optional[str]=Field(default_factory=lambda : "")    
    facebook_url:Optional[str]=Field(default_factory=lambda : "")    
    instagram_url:Optional[str]=Field(default_factory=lambda : "")  
    
      
class University(BaseDateTime , Unicreate, table=True):
   
    followers_count: Optional[int] = Field(default_factory=lambda : 0)
    haveJobPost:Optional["Universityjobs"]=Relationship(
        back_populates="university",
        sa_relationship_kwargs={
            "cascade":"all, delete-orphan"
        })
    
    
class Universityjobs(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    university_id:int = Field(default=None, foreign_key="university.id")
    job_postCount:int = Field(default=0)
    Active_jobpost:int=Field(default=0)
    expired_jobpost:int=Field(default=0)
    university:Optional["University"] = Relationship(
        back_populates="haveJobPost",
        sa_relationship_kwargs={
            "single_parent":True,
        }        
        )
    
    	
