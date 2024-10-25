from fastapi import HTTPException , status 
from sqlmodel import Session , select , and_ , or_
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from uuid import uuid4
from app.models import comment_model
from typing import Any
from app.core.app_setting import setting
from aiokafka import AIOKafkaProducer
from app.service_schemas import coment_wrapper_pb2

class CommentCrud():
    
    def get_schema_Registry_client(self):
        ...
        try:
            ...
            schema_client=SchemaRegistryClient({"url": setting.SCHEMA_REGISTRY_URL})
            return schema_client
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    
    
    def get_protobuf_serilizer(self,*,structure:Any, schema_registry_cleint:SchemaRegistryClient):
        ...    
        try:
            ...
            protobuf_serializer=ProtobufSerializer(structure, schema_registry_cleint, {"use.deprecated.format": False})
            return protobuf_serializer
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
   
   
    async def post_CommetEvent(self,*,producer:AIOKafkaProducer,event_type:str="CommentAdded", topic:str, data:comment_model.Comment_DataReceived):
        ...
        try:
            ...
            
            schema_clent=self.get_schema_Registry_client()
            
            protobuff_serilizer=self.get_protobuf_serilizer(structure=coment_wrapper_pb2.AddedComment,schema_registry_cleint=schema_clent);
            
            StructuredData=coment_wrapper_pb2.AddedComment(
                event_type=event_type,
                post_id=data.post_id,
                comment_by=data.comment_by,
                comment=data.comment,
                comment_status=data.comment_status       
               )
            
            await self.produce_event_to_kafka(producer=producer, topic=topic, protobuf_serializer=protobuff_serilizer, data=StructuredData)
            
            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e           
    
    
    
    async def produce_event_to_kafka(self,*,producer:AIOKafkaProducer,topic:str, protobuf_serializer, data:Any ):
        ...
        try:
             serilized_form=protobuf_serializer(data,SerializationContext(topic,MessageField.VALUE))            
             await producer.send_and_wait(topic, key=str(uuid4()).encode('utf-8'), value=serilized_form)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
        ...    
   
   
    def get_All_comments(self,*,postid:int, session:Session):
       ...
       try:
           ...
           if  postid:
              query:list[comment_model.Comment]=session.exec(select(comment_model.Comment).where(comment_model.Comment.post_id==postid)).all()  
              if query:
                  return  query
              else :
                  return   { 
                                "post_id" : f"{postid}" ,
                                "statement": f"no comment founf on athat post  "
                            }
                   
       except Exception as e:
           raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e                  
    
    
    
    async def post_comment(self,*,data:comment_model.Comment_DataReceived , sesison:Session,producer:AIOKafkaProducer):
        
        ...
        try:
            ...
            cmtIs:comment_model.Comment=comment_model.Comment.model_validate(data)
            
            await self.post_CommetEvent(producer=producer,event_type="CommentAdded",topic=setting.KAFKA_TOPIC_NAME2,data=data)
            
            sesison.add(cmtIs)
            sesison.commit()
            
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e    
    
    
    async def comment_DeleteEvent(self , *, producer:AIOKafkaProducer , topic:str , event_type:str="DeletedComent" , data:Any):
        
        ...
        try:
            ...
            schema_client=self.get_schema_Registry_client()
            protobuf_serilizer=self.get_protobuf_serilizer(structure=coment_wrapper_pb2.DeletedComent, schema_registry_cleint=schema_client)


            
            
            structuredData=coment_wrapper_pb2.DeletedComent(
                event_type=event_type,
                post_id=data.get("post_id"),

            )


            await self.produce_event_to_kafka(producer=producer, topic=topic, protobuf_serializer=protobuf_serilizer, data=structuredData)
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
    
    
    async def delete_comment(self,*,post_id:int ,comment_by:str ,session:Session , producer:AIOKafkaProducer):
        
        ...
        try:
            ...
            query:comment_model.Comment=session.exec(select(comment_model.Comment).where(
                and_(
                    comment_model.Comment.post_id==post_id,
                    comment_model.Comment.comment_by==comment_by,
                    ))).one_or_none()
            
            print(query)
            
            data={
                    "post_id":post_id 
                  }
            
            # print(data)
            if query :
                await self.comment_DeleteEvent(producer=producer, topic=setting.KAFKA_TOPIC_NAME2, event_type="DeletedComent", data=data)    
                session.delete(query)
                session.commit()
                return "Comment deleted"
                
            else :
                return "Comment not found"
            
            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e                  

cmt=CommentCrud()
    
