from app.Models.base import BaseIdModel
from typing import Annotated,Union
from sqlmodel import SQLModel , Field 



class PostBase(SQLModel):
      ...
      Image_type:Annotated[str,Field()] 
      pathIs:Annotated[str,Field()]
      # likecount:int|None=None
      # comment_count:Union[int,None]=None
      likecount:Annotated[Union[int,None],Field(default=None)]=None
      comment_count:Annotated[Union[int,None],Field(default=None)]=None
      share:Annotated[Union[int,None],Field(default=None)]=None

      
   


class Post(BaseIdModel,PostBase,table=True):
      ...
      userid:Annotated[int,Field()]
      

    
      

class PostReturn(SQLModel):
      id:int
      pathIs:str
      userid:int
      likecount:int|None=None
      comment_count:Union[int,None]=None
      share:Annotated[Union[int,None],Field(default=None)]    


# alembic revision -m "first migrations"


