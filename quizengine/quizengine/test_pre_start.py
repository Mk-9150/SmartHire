from sqlalchemy import Engine

from sqlmodel import Session,select, SQLModel

from quizengine.core.db_eng import engine
from quizengine.core.loggerconfig import loggerconfigu

from quizengine.init_data import init_db,initData_seed

from quizengine.models.linkmodels import QuizesTopics
from quizengine.models.topic_models import Topic 
from quizengine.models.quiz_models import Quiz


logger= loggerconfigu(__name__)


def create_tables(*,engine:Engine)->None: 
    logger.info("Creating All table")
    SQLModel.metadata.create_all(engine)
    

# def init_test_db(*,session:Session,engine:Engine):
def init_test_db(*,session:Session,engine:Engine):
    try :
        logger.info("Checking if DB is awake")
        create_tables(engine=engine)
        logger.info("Seeding the Test DB")
        
        # initData_seed(session=session)
        init_db(engine=engine)
        
    except Exception as e:
        logger.error(e)
        raise e   


def main()->None:
    logger.info("initialzing Services")
    with Session(engine) as session:
        init_test_db(session=session, engine=engine)
    # init_test_db(engine=engine)
    logger.info("initialzing Services  Finished")
    
    
    
if __name__== "__main__":
    main()
    
    
            
    