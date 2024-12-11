from aiokafka import AIOKafkaConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext , MessageField
from sqlalchemy import Engine
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from app.core.app_setting import setting
from fastapi import HTTPException , status
from app.schemas import newuser_pb2 
from app.models import Relationship_model
from sqlmodel import Session,select , and_ , or_
from sqlalchemy.orm import selectinload , joinedload 
from app.crud.AddUser import GetInUser 



def Get_Schema_Registry_Client():
    schema_registry_client=SchemaRegistryClient({
        "url":setting.SCHEMA_REGISTRY_URL
    })
    return schema_registry_client

def protobuff_Deserilizer_schema( schema_structure,schema_registry_client:SchemaRegistryClient):
     deserializer = ProtobufDeserializer(
                    schema_structure, 
                    {
                        "schema.registry.client": schema_registry_client,
                        "use.deprecated.format": False
                    }
                )
    
     return deserializer
 
async  def FeedConsumer(topic:str,KAKFA_BOOTSTRAP_SERVER , engine:Engine):
    ...
    consumer =AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAKFA_BOOTSTRAP_SERVER,
        group_id="new-users",
        auto_offset_reset="earliest",
    )
    
    await consumer.start()
    
    schema_registry_client=Get_Schema_Registry_Client()
    
    try:
        async for msg in consumer:
            if msg.topic == setting.KAFKA_TOPIC_Account_Created:
                print(f" Topic  :  ===> {msg.topic}")
                deserilizer = protobuff_Deserilizer_schema(newuser_pb2.NewUser, schema_registry_client)
                data=deserilizer(msg.value, SerializationContext(msg.topic, MessageField.VALUE))
                if data.event_type =="New_User":
                    ...
                    with Session(engine) as session:
                        ...
                        res=GetInUser.add_user(id=data.user_id, username=data.username, session=session)    
                else:
                    print("No event found to deserilize  ok ...")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from consumer code in add user user  consumer  (Feed service ) :   {str(e)}"	
        ) from e  
    
    finally:
        await consumer.stop()                      
    
    
    
     