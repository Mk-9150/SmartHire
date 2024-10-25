from sqlmodel import SQLModel , Session
from fastapi import HTTPException ,status

from app.core.db_settings import engine
from sqlalchemy import Engine
from sqlalchemy.exc   import IntegrityError 




def  initData_seed(*,session:Session):
    ...
    
def init_db(engine):
    
    try:
        with Session(engine) as session:
            logger.info("Chk Database Seeded Already !  ")
            
            # Query in any table 
            
            #  chk if return something if retuned some value then seeded already
            #  else not seeded  
            
            # initData_seed(session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        ) from e
        
           
    except Exception as e :
        logger.error(e)
        raise
                
        

if __name__ =="__main__":
    logger.info("In Initial Data Seeding Script")
    init_db(engine=engine)
    logger.info("Database Seeding Completed!")
    logger.info("Database is Working!")
    logger.info("Backend Database Initial Data Seeding Completed!")        


        
        
         
        
            