from aiokafka  import AIOKafkaConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization  import SerializationContext , MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from sqlalchemy import Engine
from fastapi  import HTTPException , status 
from sqlalchemy.orm.attributes  import flag_modified
from sqlmodel import Session  , and_ , or_ , select
from sqlalchemy.orm  import selectinload , joinedload  , Load
from app.models import Relationship_model
from app.core.app_setting import setting
from app.schemas  import postschema_pb2

def Get_Schema_RegistryClient():
    try:
        ...
        
        Registry_schemaClient:SchemaRegistryClient=SchemaRegistryClient({
            "url":setting.SCHEMA_REGISTRY_URL
        })
        
        return Registry_schemaClient
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str("error in Getting schema Registry bruh!")) from e     
    

def ProtoBuff_Deserilizer_Schema(schema_structure,RegistryClient:SchemaRegistryClient):
    ...
    try:
        ...
        
        deserilizer=ProtobufDeserializer(
            schema_structure,
            {
                "schema.registry.client":RegistryClient,
                "use.deprecated.format":False
            }
        )
        
        return deserilizer
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="error in protobyff desirilizer ")  from e 
    
    # PostCreated     
    
    
async def PostConsumer(topic:str, KAFKA_BOOTSTRAP_SERVER:str, engine:Engine):
    ...
    consumer=AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
        group_id="new-posts",
        auto_offset_reset="earliest"
    )

    await consumer.start()

    schema_registry_client=Get_Schema_RegistryClient()

    try:
        async for msg in consumer:
            if msg.topic == setting.KAFKA_TOPIC_POST_CREATED:
                deserilizer=ProtoBuff_Deserilizer_Schema(
                    postschema_pb2.PostCreated,
                    schema_registry_client
                )

                data=deserilizer(msg.value, SerializationContext(msg.topic, MessageField.VALUE))
                if data.event_type == "postCreated":
                    
                    with Session(engine) as session:
                        
            
                        ActualUser:Relationship_model.User=session.exec(select(Relationship_model.User)
                                                .options(selectinload(Relationship_model.User.haveFeed),
                                                         selectinload(Relationship_model.User.haveRelation))
                                                        #  ,Load(Relationship_model.User).raiseload("*"))
                                                .execution_options(populate_existing=True)
                                                .where(Relationship_model.User.Actualuser_id==data.user_id)).one_or_none()
                        
                        # RelationModel:Relationship_model.UserRelationship=Relationship_model.UserRelationship(followed_by=)
                        
                        followersAre=ActualUser.haveRelation.followed_by
                        if not followersAre:
                            print("No followers found")
                            if not ActualUser.haveFeed:
                                FeedModel=Relationship_model.Userfeed(feed=[data.post_id])
                                ActualUser.haveFeed=FeedModel
                                session.add(ActualUser)
                                session.commit()
                            else:
                                ActualUser.haveFeed.feed.append(data.post_id)
                                flag_modified(ActualUser.haveFeed,"feed")
                                session.add(ActualUser)
                                session.commit()
                            return
                        list_Ids_Folloowers:list[int]=list(map(lambda x:x[0] , followersAre))
                        
                        # Add postids To Followers feed 
                        
                        #1  Get Followers Object by query db 
                        Get_Followers_Object=session.exec(select(Relationship_model.User)
                                                .options(selectinload(Relationship_model.User.haveFeed))
                                                .execution_options(populate_existing=True)
                                                .where(Relationship_model.User.Actualuser_id.in_(set(list_Ids_Folloowers)))).all()
                        
                        for follower in Get_Followers_Object:
                            if not follower.haveFeed:
                                FeedModel=Relationship_model.Userfeed(feed=[data.post_id])
                                follower.haveFeed=FeedModel
                            else :
                                follower.haveFeed.feed.append(data.post_id)
                                flag_modified(follower.haveFeed, "feed")
                        
                        if not ActualUser.haveFeed:
                            FeedModel=Relationship_model.Userfeed(feed=[data.post_id])
                            ActualUser.haveFeed=FeedModel
                            # session.add(ActualUser)
                            # session.commit()
                        else:
                            ActualUser.haveFeed.feed.append(data.post_id)
                            flag_modified(ActualUser.haveFeed,"feed")
                            
                        # session.add(ActualUser)
                        Get_Followers_Object.append(ActualUser)
                        session.add_all(Get_Followers_Object)
                        session.commit()            
     
                else:
                    print("No event found to deserilize  ok ...")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from consumer code in Feed  post Consumer: {str(e)}"	
        ) from e  
    
    finally:
        await consumer.stop()      