from sqlmodel import SQLModel , Field
from app.models.base import BaseModel
from typing import Annotated

class likeBase(SQLModel):
    post_id:int
    like_status:Annotated[bool , Field(default=False)]
    
class Like(BaseModel,likeBase,table=True):
        
        likedBy:str
                

class receiveData(SQLModel):  #  the model for like post 
    post_id:int
    likedBy:str
    like_status:bool
    
class unlikeData(SQLModel): # the model for like post
    post_id:int
    un_likedBy:str
    like_status:bool    

    
    
    
         
        