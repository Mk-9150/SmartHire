from quizengine.crud.topicCrud import quizTpic
from quizengine.models.topic_models import (
    Topic ,
    TopicCreate,TopicResponse,
    TopicResponseWithQueations,
    TopicUpadate
)
from quizengine.core.loggerconfig import loggerconfigu 
from quizengine.api.deps import DbDependency 
from typing import Annotated 

from fastapi import Depends , APIRouter ,HTTPException,Query,Path

router= APIRouter()

logger=loggerconfigu(__name__)
@router.post("/create")
def createTopic(topicData:TopicCreate,db:DbDependency):
    """
    Create a new recursive topic.

    Args:
        topic (TopicCreate): The topic data to create.

    Returns:
        TopicResponse: The created topic.

    Raises:
        HTTPException: If an error occurs while creating the topic.
    """
    logger.info("%sloggers.create_a_topic: %s", __name__, topicData)
    
    try:
        
        created_Topic=quizTpic.createTopic(topicData=topicData,db=db)
        return created_Topic
        
    except ValueError as e : 
        logger.error(f"Error creating topic: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as httperr:
        logger.error(f"Error creating topic: {httperr}")
        raise httperr
    except Exception as e:  # Catching any unexpected errors
        logger.error(f"Unexpected error creating topic: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")



@router.get("/allTopic",) 
def ReadAllTopicPerPage(*,
                        page:int=Query(
                            default=1,
                            description="Page  number " ,
                            ge=1
                            ) ,
                        per_page:int=Query(
                            default="10",
                            description="Item per page ",
                            ) ,
                        db:DbDependency
                        ):
    """
    Get all topics.

    Args:
        offset (int, optional): The offset for pagination. Defaults to 0.
        limit (int, optional): The limit for pagination. Defaults to 100.

    Returns:
        PaginatedTopicRead: The list of topics paginated.

    Raises:
        HTTPException: If an error occurs while retrieving topics.
    """
    
    logger.info("%s.get_topics: triggered", __name__)
    
    try:
            offset=(page-1) * per_page;
            all_Records=quizTpic.read_Topics(offset=offset , per_page=per_page,db=db)
            count=quizTpic.countAllTopic(db=db)
                         
             #  calculate the Url for Next Or previous Pages:
             
            next_page=f"?page={page+1}&per_page={per_page}" if len(all_Records) > 0 <=per_page else None
            pervious_page=f"?page={page-1}&per_page={per_page}" if page>1 else None
            
            
            paginated_Data={
                "count":count,
                "next":next_page,
                "pre":pervious_page,
                "result":all_Records
            }
        
    except HTTPException as http_err:
        logger.error(f"Error retrieving topics: {http_err}")
        raise http_err  # Re-raise the HTTPException with the original status code and detail
    except Exception as e:
        logger.error(f"Unexpected error retrieving topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topics.")
    
    
@router.get("/{topicId}")
def getTopicById(topicId:Annotated[int,Path()],db:DbDependency):
    """
    Get a topic by ID.

    Args:
        topicId (int): The ID of the topic to retrieve.

    Returns:
        TopicResponse: The retrieved topic.

    Raises:
        HTTPException: If an error occurs while retrieving the topic.
    """
    logger.info("%s.get_topic_by_id: triggered", __name__)
    
    return quizTpic.getTopicById(tid=topicId,db=db)


    try:
        topic=quizTpic.getTopicById(topicId=topicId, db=db)
        return topic
    except HTTPException as http_err:
        logger.error(f"Error retrieving topic: {http_err}")
        raise http_err  # Re-raise the HTTPException with the original status code and detail
    except Exception as e:
        logger.error(f"Unexpected error retrieving topic: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topic.")
    
    
        
@router.get("/{topicId}/subtopics")
def TopicAndSubTopics(*,topicId:int=Path(),db:DbDependency):
    
    logger.info("%s.get_topic_and_subtopics: %s", __name__, topicId)
    
    try:
        topic_and_subtopics=quizTpic.readTopicAndSubTopic(topicId=topicId, db=db)
        
        # print("\n\n\n ---------------------------------------------------------------------------------------------------------------------------------------\n\n")
        # print(dict(topic_and_subtopics))
        
        return topic_and_subtopics
   
    except HTTPException as http_err:
        logger.error(f"Error retrieving topics: {http_err}")
        raise http_err
   
   
    except Exception as e:
        logger.error(f"Unexpected error retrieving topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topics.")
   
   
    
@router.patch("/update/{topicId}")
def UpdateTopic(topicId:Annotated[int,Path()] ,updatingData:TopicUpadate,db:DbDependency):
    """
    Update a topic by ID.

    Args:
        topic_id (int): The ID of the topic to update.
        topic (TopicUpdate): The updated topic data.

    Returns:
        TopicResponse: The updated topic.
    """
    logger.info("%s.update_topic_by_id: %s", __name__, topicId
                )
    try:
   
        return quizTpic.UpdateTopicById(Topicid=topicId,db=db,data=updatingData)
   
    except ValueError:
   
            db.rollback()
            logger.error("UPDATE_TOPIC: Topic not found")
            raise ValueError("Topic not found")
   
    except SQLAlchemyError as e:
   
            db.rollback()
            logger.error(f"UPDATE_TOPIC: Error updating topic: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating topic {str(e)}",
            )
   
    except Exception as e:
   
            db.rollback()
            logger.error(f"UPDATE_TOPIC: Error updating topic: {str(e)}")
            raise Exception("Error updating topic")
        
        
        
@router.delete("/delete/{topicId}")
def deleteTopicById(topicId:Annotated[int,Path()],db:DbDependency):
    """
        Deletes a topic from the database based on the provided ID.

        Args:
            topicId (int): The ID of the topic to be deleted and remove connection to the child also if parent id Given  .
            topicId (int): The ID of the topic to be deleted and remove connection to the child also parent also  if child id Given  .
            
            db (optional) : Database Dependency Injection.

        Raises:
            HTTPException: If the topic with the provided ID is not found.

        Returns:
            dict: A dictionary with a message indicating the successful deletion of the topic.
    """
    logger.info("%s.delete_topic_by_id: %s", __name__, topicId)
    
    try:
        
        quizTpic.deleteTopic(topicId=topicId,db=db)
    
    except HTTPException as e :
        
        logger.error(f"DELETE_TOPIC: {e}")
        raise e
  
    except Exception as e:
        
        logger.error(f"Unexpected error deleting topic: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete topic.")
        
        
        
        
        
       
   
           
