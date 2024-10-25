from app.core.db_settings import engine
from sqlalchemy import Engine
from sqlmodel import SQLModel

from app.models.TeaUniLink import TeacherUniLink
from app.models.TeacherModel import Teacher 
from app.models.Institute_model import Institute 
from app.core.settings import setting
from app.core.loggerConfig import loggeng


logger=loggeng(__name__)




def createTables(*,engine:Engine):  
    
    logger.info("Creating The Tables ")
    SQLModel.metadata.create_all(engine)
    

def  init_test_db(*,engine:Engine):
    
    createTables(engine=engine)
    
    
    # logger.info("Seeding the Test DB")
    
    # init_db(engine=engine)
        
    ...   
    
def main():
    
    logger.info("Initializig Services ")
    init_test_db(engine=engine)    
    logger.info("Initializig Finished ")

    ...   
    
if __name__=="__main__":
    main()
         

  