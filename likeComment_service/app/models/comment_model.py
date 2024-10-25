from sqlmodel import SQLModel , Field
from typing import Annotated
from app.models.base import BaseModel

class CommentBase(SQLModel):
    post_id:int
    comment_status:Annotated[bool , Field(default=False)]
    
class Comment(BaseModel,CommentBase,table=True):
        ...
        comment_by:str
        comment:str
        


   
class Comment_DataReceived(SQLModel):
     ...
     post_id:int
     comment_by:str
     comment:str
     comment_status:bool                             
        