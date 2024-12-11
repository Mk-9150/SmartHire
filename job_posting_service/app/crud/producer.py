from confluent_kafka.serialization import SerializationContext ,MessageField 
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf  import ProtobufSerializer
from typing import  Annotated , Optional 
from app.core.app_setting  import setting 
from app.models import model
from fastapi import HTTPException , status
from aiokafka import AIOKafkaProducer
from app.schemas  import applier_sch_pb2 #.Applier
from uuid  import uuid4

class KafkaProducer():
    ...
        
        
    def get_schma_client(self):
        try:
            
            schema_registry_client=SchemaRegistryClient({"url":setting.SCHEMA_REGISTRY_URL})
            return schema_registry_client    
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something happend  unexpected in getting schema registry client at job posting producer {str(e)}"
            ) from e
            
    def GET_protobuffSerilizer(self,*,structure,schema_registry_client):
        try:
            protobuf_serializer=ProtobufSerializer(structure,schema_registry_client,{"use.deprecated.format":False})
            return protobuf_serializer
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something happend  unexpected in getting protobuf serializer at job posting producer {str(e)}"
            ) from e    
            
    async def postEvent(self , applier_iid:int , userid:int,username:str,producer:AIOKafkaProducer , topic:str):
        ...
        schemaClient=self.get_schma_client()
        protobuf_serializer=self.GET_protobuffSerilizer(structure=applier_sch_pb2.Applier, schema_registry_client=schemaClient)
        try:
            applier=applier_sch_pb2.Applier(event_type="Applied" , applier_id=applier_iid , user_id=userid , username=username)
            await self.ProducedMessage(producer=producer, topic=topic, protobuf_serializer=protobuf_serializer, message=applier)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something happend  unexpected in getting protobuf serializer at job posting producer {str(e)}"
            ) from e
        
        
        
    async  def ProducedMessage(self, *, producer:AIOKafkaProducer, topic:str, protobuf_serializer, message):
        try:
            ...
            payload=protobuf_serializer(message, SerializationContext(topic, MessageField.VALUE))
             
            await producer.send_and_wait(topic,key=str(uuid4()).encode('utf-8'),value=payload)  
            
        except  Exception as e:
            print(f"Error producing message: {str(e)}")
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}" )  from e

Prodducer=KafkaProducer()    