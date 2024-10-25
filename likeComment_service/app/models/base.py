from sqlmodel import SQLModel , Field
from typing import Optional , Union , Annotated , Any , Literal
from datetime import datetime
class BaseModel():
    ...
    id:Annotated[Union[int,None] , Field(default=None , primary_key=True)]
    likeAt:datetime = Field(default_factory=datetime.now)
    