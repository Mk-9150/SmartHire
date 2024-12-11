from app.Models.base import BaseIdModel 
from typing import Annotated,Union
from sqlmodel import SQLModel , Field , Relationship
import datetime
from pydantic import model_validator


class PostBase(SQLModel):
      ...
      Image_type:Annotated[str,Field()] 
      pathIs:Annotated[str,Field()]
      
      likecount:Annotated[Union[int,None],Field(default=None)]=None
      comment_count:Annotated[Union[int,None],Field(default=None)]=None
      share:Annotated[Union[int,None],Field(default=None)]=None
      # time_zone:Annotated[str,Field(default=None)]
      
class TimePlus_TimeZone(SQLModel):
      timezone:str=Field(default_factory=str)
      localTime:str=Field(default_factory=str)  #  this utc_time   represemt localTime        
# class TimePlus_TimeZone_datetime(SQLModel):
      # time_zone:str=Field(default_factory=str)
      # utc_ime:datetime.datetime=Field(default_factory=datetime.datetime)      
      
class UtcTime_timezone_Create(SQLModel):      
      time_zone:Annotated[str,Field(default=None)]
      utc_time:str  #  from front-end  this will catch local time   then it will be converted to utc_time 


class UtcTime_timezone_Model(UtcTime_timezone_Create):
      
      @model_validator(mode="after")
      def  isoFormetTo_datetime(self):
            if isinstance(self.utc_time, str):
                  self.utc_time =datetime.datetime.fromisoformat(self.utc_time)
                  return self

class UtcTime_timezone(SQLModel, table=True):
      ...     
      
      id:Annotated[int,Field(primary_key=True, default=None)]
      time_zone:Annotated[str,Field(default=None)]
      utc_time:datetime.datetime
      post_id:Annotated[int,Field(foreign_key="post.id")]
      post:"Post" = Relationship(back_populates="haveTime")
      
      
      
      # @model_validator(mode="after")
      # def  isoFormetTo_datetime(self):
      #       self.utc_time =datetime.datetime.fromisoformat(self.utc_time)
      #       return self
      


class Post(BaseIdModel,PostBase,table=True):
      ...
      userid:Annotated[int,Field()]
      
      haveTime:"UtcTime_timezone"=Relationship(
            back_populates="post",
            sa_relationship_kwargs={
                  "cascade":"all, delete-orphan"
            }
      )
      

class getLastweekPOst(SQLModel):
      # id:int
      # pathIs:str
      # userid:int
      # likecount:int|None=None
      # comment_count:Union[int,None]=None
      # share:Annotated[Union[int,None],Field(default=None)]  
      # time_timezone=
      ...
      
class PostReturn(SQLModel):
      id:int
      pathIs:str
      userid:int
      likecount:int|None=None
      comment_count:Union[int,None]=None
      share:Annotated[Union[int,None],Field(default=None)]  
      haveTime:TimePlus_TimeZone=Field(default_factory=TimePlus_TimeZone)
      # time_zone:Annotated[str,Field(default=None)]
      # utc_time:datetime.datetime
        


# alembic revision -m "first migrations"


