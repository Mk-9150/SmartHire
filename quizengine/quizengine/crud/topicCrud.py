from sqlmodel import SQLModel ,Session,select
from quizengine.models.topic_models import (
    Topic ,
    TopicCreate,TopicResponse,
    TopicResponseWithQueations,
    TopicUpadate
)
from sqlalchemy.orm import selectinload
from quizengine.core.loggerconfig import loggerconfigu
from typing import Any
from sqlalchemy.exc import SQLAlchemyError ,  IntegrityError
from fastapi import HTTPException,status
logger= loggerconfigu(__name__)


class QuizTopicCrud:
    def createTopic(self,*,topicData:Any,db:Session):
        
        try:
            
            if topicData:
                RealTopic=Topic.model_validate(topicData)
                
                db.add(RealTopic)
                db.commit()
                db.refresh(RealTopic)
                return RealTopic
        
       
      
        except IntegrityError as e:
            #  This error will be shown when there is integrity issue  , contraints  voilations
            # Primary key violation: Trying to insert a row with a duplicate value for the primary key.
            # Unique constraint violation: Inserting data that violates a unique constraint defined on a column or set of columns.
            # Foreign key constraint violation: Attempting to create a foreign key relationship that references a non-existent row in another table.
      
            db.rollback()
            logger.error("%s  An integrity Error Occured while Creating the Topic    %s  : ",str(e))
            raise ValueError("Data Integrity Issue ")  from e    
        
        
       
        except SQLAlchemyError as e:
            # SqlAlchemy Error  :
            # Common Causes:
            # Connection errors: Issues establishing a connection to the database server.
            # Programming errors: Mistakes in your SQLAlchemy code, like using incorrect syntax or methods.
            # Data type mismatches: Attempting to insert data into a column with a type mismatch (e.g., trying to insert a string into an integer column).
            # Schema reflection issues: Problems during automatic schema reflection from the database.
            
            db.rollback()
            logger.error("%s  A dataBase Error   Occured while Creating the Topic    %s  : ",str(e))
            raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail=f"DataBase related Error   {str(e)}"   
            )
       
       
        except Exception as e:
            db.rollback()
            logger.error("%s An Unexpected Error Occured  %s  ",str(e))
            raise Exception("An unexpected Erorr Occured") from e
        
    def read_Topics( self,*,offset:int ,per_page:int , db:Session):
            try:
                
                if offset < 0 :
                   raise HTTPException(status_code=400, detail="Offset cannot be negative")
                if per_page < 1:
                   raise HTTPException(status_code=400, detail="Per page items cannot be less than 1")
                
                topics= db.exec(select(Topic).offset(offset).limit(per_page)).all() 
                if not topics:
                    raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No topics found"
                    )
                return topics
            except HTTPException as e:
                db.rollback()
                logger.error(f"READ_TOPICS: No topics found: {e}")
                raise e  # Re-raise the HTTPException with the original status code and detail
          
            except SQLAlchemyError as e:
                db.rollback()  # Ensure rollback is awaited
                logger.error(
                    f"READ_TOPICS: A database error occurred while retrieving topics: {e}"
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database operation failed. {str(e)}",
                )       
          
          
            except Exception as e:
                db.rollback()
                logger.error("%s Read_Topic:  An unexpedted Error Occured  %s ")   
                raise Exception("An unexpedted Error Occured")  from e 


    def  countAllTopic(self,*,db:Session):
        try:
            allTopics=db.exec(select(Topic.title)).all()
            count= len(allTopics)
            return count
        except Exception as e:
            db.rollback()
            print(f" An unexpected Error occur  counting SearchToolRecord items: {e}")
            # Re-raise the exception to be handled at the endpoint level
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
         
         
         
         
    def getTopicById(self,*,tid:int , db:Session) :
        
        try:
            
            topicbyID:Topic=db.exec(
                select(Topic).where(Topic.id==tid)
            ).one_or_none()
            if not topicbyID:
                raise ValueError("Topic not Found")
            
            return topicbyID
        except ValueError as e:
            db.rollback()
            logger.error(f"GET_TOPIC_BY_ID: Topic not found: {e}")
            raise HTTPException(status_code=404, detail=str(e)) from e
       
        except SQLAlchemyError as e:
            db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            ) from e
       
        except HTTPException as http_err:
            db.rollback()
            raise http_err
       
        except Exception as e:
            db.rollback()  # Ensure rollback is awaited
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            ) from e            
            
    
    
    
    def readTopicAndSubTopic(self,*,topicId:int,db:Session):
        
        """
        ####   Fetch Topic with Subtopic   with below Structure 
         {
                "topic_id": topicResult.id,
                "title": topicResult.title,
                "description": topicResult.description,
                "parent_topic_id": parent_topic_id,
                # "children_topic_ids": children_topic_ids,
                "children_topics": [
                      {
                        "topic_id": topicResult.id,
                        "title": topicResult.title,
                        "description": topicResult.description,
                        "parent_topic_id": parent_topic_id,
                        # "children_topic_ids": children_topic_ids,
                        "children_topics": [
                                 {
                                    "topic_id": topicResult.id,
                                    "title": topicResult.title,
                                    "description": topicResult.description,
                                    "parent_topic_id": parent_topic_id,
                                    # "children_topic_ids": children_topic_ids,
                                    "children_topics": [], 
                                }      
                            
                            ], 
                      },
                      {
                        "topic_id": topicResult.id,
                        "title": topicResult.title,
                        "description": topicResult.description,
                        "parent_topic_id": parent_topic_id,
                        # "children_topic_ids": children_topic_ids,
                        "children_topics": [], 
                      }            
                    ], 
            }                      
        
        """
        try:
                
            topicResult=db.exec(
                select(Topic)
                .options(
                    selectinload(Topic.children_topics),
                    selectinload(Topic.parent_topic)
                )
                .where(Topic.id==topicId)
            ).one_or_none()
            
            if  not topicResult :
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
                )
                
            # print(topicResult.children_topics)
            # print("\n\n\n\n  ----------------------------------------------------------------------------- \n\n\n")
                
            # print(topicResult.parent_topic)
            
            
            parent_topic_id:int = topicResult.parent_topic.id if topicResult.parent_topic else None

            childTopics:list[Topic]=[]
                
            if topicResult.children_topics:
                for child in topicResult.children_topics:
                         childTopic=self.readTopicAndSubTopic(topicId=child.id , db=db)
                         childTopics.append(childTopic)

            
            return {
                "topic_id": topicResult.id,
                "title": topicResult.title,
                "description": topicResult.description,
                "parent_topic_id": parent_topic_id,
                # "children_topic_ids": children_topic_ids,
                "children_topics": childTopics, 
            }            
            
            # this code also correct both use recursion for fetching topic and subtopic  bu this below code fetch topic its childs then childs k childs  and store it all  in the array  
            # def gettingSubtopics(topicIds:list[int],db:Session):
            #      nonlocal childTopics 
            #      subtopics=db.exec(
            #         select(Topic)
            #         .options(
            #              selectinload(Topic.children_topics)
            #         )
            #         .where(Topic.id.in_(topicIds))
            #      )
                 
            #      for topic in subtopics :
                     
            #          childTopics.append(topic)
            #          if topic.children_topics:
            #            gettingSubtopics([child.id for child in topic.children_topics ])
                         
            
            # if topicResult :
            #     childTopics.append(topicResult);
                
            #     gettingSubtopics([topic.id for topic in topicResult.children_topics])
            
            
           
            
                        
            
        except  ValueError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        
        except HTTPException as http_err:
            db.rollback()
            raise http_err    
        
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
            
            
            
    def UpdateTopicById(self,*,Topicid:int,db:Session,data:TopicUpadate):
        
        """
        Update a topic in the database.

        Args:
            id (int): The ID of the topic to update.
            topic (TopicUpdate): The updated topic data.
            db (optional) : Database Dependency Injection.

        Returns:
            Topic: The updated topic.

        Raises:
            ValueError: If the topic with the given ID is not found.
        """
        
        try:
            topic:Topic=db.get(Topic,Topicid)
            
            if not topic:
                raise ValueError("Topic not Found")
            
            for key , value in data.model_dump(exclude_unset=True).items():
                 if hasattr(topic,key):
                     setattr(topic,key,value)
            
          
            db.add(topic)
            db.commit()
            db.refresh()
            return topic
             
     
        except ValueError as e:       
            db.rollback();
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
    
    
    
    
    
    def _removeRelationParentChild(self,*,topic:Topic,db:Session):
        """
            #  :  if parent topic  given  (topic)  Remove The Relationship  to the childs  and delete the topic make parent.childtopic=None 
            #  :  if child tpic given then remove relationship to the parent and also remove the relation to its childs :
        
        """
    
        if topic:
            parentTopic =topic.parent_topic if topic.parent_topic else None
            if not parentTopic :
              if  topic.children_topics:
                for child in topic.children_topics:
                    child.parent_id = None
        
              db.delete(topic)
              db.commit()
            
            if parentTopic :
                topic.parent_topic=None
                db.delete(topic)
                db.commit()
              
            
    def deleteTopic(self,*,topicId:int,db:Session):
        try:
            ...
            topic:Topic=db.exec(
                select(Topic)
                .options(
                    selectinload(Topic.children_topics),
                    selectinload(Topic.parent_topic)
                )
                .where(Topic.id ==topicId)
            ).one_or_none()
            
            if not topic:
                raise HTTPException(
                    status_code=HTTP_404_NOT_FOUND 
                    , detail="Topic not Found"
                )
            
            
            
            self._removeRelationParentChild(topic=topic,db=db)
            
            return topic
            
            
        except HTTPException as httpErr:
            db.rollback()
            raise  HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
            )
            
        except Exception as  e:
            
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting topic",
            ) 
                 
            
quizTpic=QuizTopicCrud()
        