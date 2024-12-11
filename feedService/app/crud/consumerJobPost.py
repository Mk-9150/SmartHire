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
    
    
async def JobPostConsumer(topic:str, KAFKA_BOOTSTRAP_SERVER:str, engine:Engine):
    ...
    consumer=AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
        group_id="new-jobposts",
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
                if data.event_type == "Applied":
                    ...
                    with Session(engine) as session:
                        ...
#     
                        ActualUser:Relationship_model.User=session.exec(select(Relationship_model.User)
                                                .options(selectinload(Relationship_model.User.isapplier)
                                                         , Load(Relationship_model.User).raiseload("*")
                                                         )
                                                .execution_options(populate_existing=True)
                                                .where(Relationship_model.User.Actualuser_id==data.user_id)).one_or_none()
                        
                        if not ActualUser:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
                        else:
                                                    
                            if not ActualUser.isapplier:
                                ActualUser.isapplier=Relationship_model.UserJOBPost(appliedTo_id=[(data.applier_id,data.jobpost_id)])
                                session.add(ActualUser)
                                session.commit()
                            else:
                                ActualUser.isapplier.appliedTo_id.append((data.applier_id, data.jobpost_id))
                                flag_modified(ActualUser.isapplier, "appliedTo_id")
                                session.add(ActualUser)
                                session.commit()
                                
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from consumer code in Feed  post Consumer: {str(e)}"	
        ) from e  
    
    finally:
        await consumer.stop()                 
        
# comsumerJobPost=JobPostConsumer     