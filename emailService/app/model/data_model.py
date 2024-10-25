from sqlmodel import SQLModel,Field
from typing import Annotated , Union  

class Account(SQLModel):
    username:str
    email:str
    # description:str
    
    