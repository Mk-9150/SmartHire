from fastapi import HTTPException , status
from sqlmodel import Session ,select , and_
from app.models import like_mode 
from confluent_kafka.schema_registry import SchemaRegistryClient 
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import SerializationContext ,MessageField 
from uuid import uuid4
from app.core.app_setting import setting
from typing import Any
from aiokafka import AIOKafkaProducer
from app.service_schemas.like_unlike_post_pb2 import LikePosted , UnlikePosted
# from app.service_schemas import post_like_pb2
# from app.service_schemas import post_unlike_pb2

class LikeCrud():
    
    
    def get_schema_Registry_client(self):
        ...
        try:
            schema_client=SchemaRegistryClient({"url":setting.SCHEMA_REGISTRY_URL})
            return schema_client
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e
    
    
    # async def produce_serilize_protobuff_message_to_kafka(self,*,producer:AIOKafkaProducer,topic:str,protobuf_serializer,data,partition:int):
    # async def produce_serilize_protobuff_message_to_kafka(self,*,producer:AIOKafkaProducer,topic:str,protobuf_serializer,data):
    #     ...
    #     """
    #     Produces a Protobuf message asynchronously to a Kafka topic.
    #     """
    #     try:
    #         payload = protobuf_serializer(data, SerializationContext(topic, MessageField.VALUE))
    #         await producer.send_and_wait(topic, payload)
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e
    
    def get_protobuf_serilizer(self,*,structure, schema_registry_cleint:SchemaRegistryClient):
        ...
        try:
            
            protobuf_serializer = ProtobufSerializer(structure, schema_registry_cleint, {"use.deprecated.format": False})
            return protobuf_serializer
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e} : eror at get protobuf serilizer  " )  from e
    
    
    async def postEvent(self,*,postid:int , likeby:str ,likestatus:bool, eventType:str, producer:AIOKafkaProducer,topic:str):
        ...
        try:
            ...
            schema_client=self.get_schema_Registry_client()
            # protobuff_serilizer=self.get_protobuf_serilizer(structure=post_like_pb2.LikePosted, schema_registry_cleint=schema_client)
            protobuff_serilizer=self.get_protobuf_serilizer(structure=LikePosted, schema_registry_cleint=schema_client)
            
            StructuredData=LikePosted(
                event_type =eventType,
                post_id = postid,
                liked_by = likeby,
                liked_status = likestatus
            )
            
            
            
        # await self.produce_serilize_protobuf_messgae_to_kafka(producer=producer,topic=topic,protobuf_serializer=protobuff_serilizer,data=postData,partition=partition)
            await self.produce_serialize_event_to_kafka(producer=producer, topic=topic, protobuf_serializer=protobuff_serilizer, data=StructuredData)
          
          
            # protobuf_serializer = ProtobufSerializer(Like, schema_client, {"use.deprecated.format": False})
            # producer = AIOKafkaProducer(
            #     bootstrap_servers=setting.KAFKA_BOOTSTRAP_SERVERS,
            #     value_serializer=lambda v: protobuf_serializer(v, SerializationContext("like", MessageField.VALUE))
            # )
            # await producer.start()
            # return producer
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e
            
    
    async def produce_serialize_event_to_kafka(self,*,producer:AIOKafkaProducer,topic:str, protobuf_serializer, data:Any ):
        ...
        try:
            ...
            payload=protobuf_serializer(data, SerializationContext(topic, MessageField.VALUE))
            # await producer.send_and_wait(topic, payload
            await producer.send_and_wait(topic, key=str(uuid4()).encode('utf-8'), value=payload,)
            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e
    
    
    
    def getAllLikeOfPost(self,*,postid:int  , session:Session):
        ...

        try:
            ...
            likesData:like_mode.Like=session.exec(select(like_mode.Like).where(like_mode.Like.post_id==postid)).all()
            if not likesData:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
            return likesData
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))    from e    
        
    
    
    
    
    
    async def postLike(self, *, like:like_mode.receiveData, session:Session,producer:AIOKafkaProducer):
        
        
        try:
            ...
           
            likeToDatabase:like_mode.Like=like_mode.Like.model_validate(like)
            
            await self.postEvent(postid=likeToDatabase.post_id, likeby=likeToDatabase.likedBy, likestatus=likeToDatabase.like_status, eventType="Liked", producer=producer, topic=setting.KAFKA_TOPIC_NAME)            
            session.add(likeToDatabase)
            session.commit()
            session.refresh(likeToDatabase)
            return like

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e    



    async def post_Unlike_Event(self,*,postid:int,producer:AIOKafkaProducer,topic:str,eventType:str="Unliked"):
        ...
        
        try:
            ...
            schema_Client=self.get_schema_Registry_client()
            protobuf_serilizer=self.get_protobuf_serilizer(structure=UnlikePosted, schema_registry_cleint=schema_Client)
            structuredData=UnlikePosted(
                event_type=eventType,
                post_id=postid
            )
            await self.produce_serialize_event_to_kafka(producer=producer, topic=topic, protobuf_serializer=protobuf_serilizer, data=structuredData) 

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e
        
    
    
    async def postUnlike(self, *, postid:int,dislikeBy:str , session:Session , producer:AIOKafkaProducer):
                
        try:
            ...
            # return "ddd"
            # postUnliked:list[like_mode.Like]=session.exec(select(like_mode.Like).where(
            #     and_(
            #         like_mode.Like.post_id==postid,
            #         like_mode.Like.likedBy==dislikeBy
            #     )
            #  )).all()     
            postUnliked:like_mode.Like=session.exec(select(like_mode.Like).where(
                and_(
                    like_mode.Like.post_id==postid,
                    like_mode.Like.likedBy==dislikeBy
                )
             )).one_or_none()

            if not postUnliked:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")      
            
            
            await self.post_Unlike_Event(postid=postid, producer=producer, topic=setting.KAFKA_TOPIC_NAME)
                       
            # for entry in postUnliked:            
            #     session.delete(entry)
            #     session.commit()
            session.delete(postUnliked)
            session.commit()
            

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e    

    

lke=LikeCrud()        