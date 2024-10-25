from sqlmodel import SQLModel , Session
from typing import Annotated
from app.core.db_settings import engine
from fastapi import Depends





def SessionDependency():
    """
        
        ---->>   This is a Session Dependency for Crud Operations in database 
        
        ---->>    With this session we can add delete , update ,Read 

         
    """
    
    with Session(engine) as session:
        print("nice")
        yield session
    
    
    
    ...        
    
    

SessionEngine=Annotated[Session,Depends(SessionDependency)]
