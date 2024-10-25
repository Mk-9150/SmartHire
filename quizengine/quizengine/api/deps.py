from quizengine.core.db_eng import engine

from sqlmodel import SQLModel , Session
from typing import Annotated
from fastapi import Depends



#  Session Dependency !

def Get_Session():
    with Session(engine) as session:
        yield session
    
    
DbDependency=Annotated[Session,Depends(Get_Session)]



        