from sqlmodel import SQLModel,Field 
from typing import Annotated , Union 
from datetime import datetime 

class BaseModelID(SQLModel):
    id:Union[int|None]=Field(default=None,primary_key=True)
    created_at:datetime=Field(default_factory=datetime.now)
    updated_at:datetime=Field(default_factory=datetime.utcnow , sa_column_kwargs={"onupdate":datetime.now})
    
    