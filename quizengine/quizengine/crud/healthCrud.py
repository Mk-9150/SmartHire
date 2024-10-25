from quizengine.models.health_models import (
    Health,Status,Stats
)

from quizengine.core.loggerconfig import loggerconfigu
from sqlmodel import Session,text
from quizengine.settings import ENV

logger=loggerconfigu(__name__)



def get_Health(db:Session):
    
    db_status=health_db(db=db)
    logger.info("%s Db Status  %s : ", __name__,db_status)
    
    return Health(app_status=Status.OK , db_status=db_status , environment=ENV) 


def getStats(db:Session):
    stats=Stats(
        topic=countFromDb("topic",db),
        questionbank=countFromDb("questionbank",db),
        mcqoption=countFromDb("mcqoption",db),
    )
    # topic = countFromDb("topic",db)
    # print(stats)
    # print(topic)
    
def countFromDb(table:str,db:Session):
    
    count=db.exec(text(f"SELECT COUNT(id)  from {table}"))
    
    if  count is None:
        return 0
    
    # objs=count.scalars().one_or_none()   # output e.g 2 
    # objs=count.scalar(); #output e.g 2
    objs=count.one_or_none(); #output  (2,)  if reocrds of topic 2 in db else depend on hiw mamny are there
    print(type(objs),objs)
    
    return objs if isinstance(objs,int) else objs[0] if objs else 0
   
    # if isinstance(objs,int):
    #     return objs
       


def health_db(db:Session):
     
     try:
         db.exec(text("SELECT COUNT(id)  from topic"))
         return Status.OK
     except Exception as e:
         logger.error(f"Health DB Error: {e}")     
     return Status.NOT_OK
    