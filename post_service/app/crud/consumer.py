from aiokafka import AIOKafkaConsumer
from app.core.app_settings import setting
from fastapi import HTTPException, status
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from app.service_schema.like_unlike_post_pb2 import LikePosted, UnlikePosted
from app.service_schema.coment_wraper_pb2 import AddedComment , DeletedComent
from  sqlmodel import  Session , select , and_ , or_ 
from sqlalchemy import Engine
from app.Models.post_model import Post
def get_schema_registry_client():
    schema_registry_client = SchemaRegistryClient({
        'url': setting.SCHEMA_REGISTRY_URL
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
 

async def L_consumer(topic: str,topic2:str, BOOTSTRAP_SERVER_KAFKA_URL,engine:Engine):
    print("Inside consumer")
    consumer = AIOKafkaConsumer(
        topic,topic2,
        bootstrap_servers=BOOTSTRAP_SERVER_KAFKA_URL,
        group_id="my-group",
        auto_offset_reset="earliest",
    )

    await consumer.start()

    schema_registry_client = get_schema_registry_client()


    try:
        async for msg in consumer:
            if msg.topic=="liked":
                print("Processing mes/sage...")
                # Deserialize the message value
                deserializer = protobuff_Deserilizer_schema(LikePosted, schema_registry_client)
                data = deserializer(msg.value, SerializationContext(msg.topic, MessageField.VALUE))
                if data.event_type=="Liked":
                    print(f"Deserialized data: {data}")
                    with Session(engine) as session:
                        # query=session.exec(select(Post).where(Post.id==data.post_id)).one_or_none()
                        query:Post=session.get(Post, data.post_id)
                        if not query:
                            print("Post not found")
                        else :
                                query.likecount +=1
                                session.add(query)
                                session.commit()
                elif data.event_type=="Unliked":
                    unlikedeserializer = protobuff_Deserilizer_schema(UnlikePosted, schema_registry_client)
                    data= unlikedeserializer(msg.value,SerializationContext(topic,MessageField.VALUE))               
                    with Session(engine)  as session:
                        query:Post=session.get(Post, data.post_id)
                        if not query:
                            print("Post not found")
                        else :
                            if query.likecount==0:
                                pass
                            elif query.likecount==1:
                                    query.likecount=0
                            else:
                                query.likecount -=1
                            session.add(query)
                            session.commit()      
                else:
                    print("No data returned after deserialization.")
            elif msg.topic=="commented":
                ...
                Cmt_deserilizer=protobuff_Deserilizer_schema(AddedComment , schema_registry_client)
                cmt_data=Cmt_deserilizer(msg.value ,SerializationContext(topic2 , MessageField.VALUE))
                if cmt_data.event_type=="CommentAdded":
                    with Session(engine) as session:
                        query:Post=session.get(Post, cmt_data.post_id)
                        if not query:
                            print("Post not found")
                        else :
                                query.comment_count+=1
                                session.add(query)
                                session.commit()
                elif cmt_data.event_type=="DeletedComent":
                    deleted_cmt_deserilizer=protobuff_Deserilizer_schema(DeletedComent, schema_registry_client)
                    dlete_cmt_event=deleted_cmt_deserilizer(msg.value, SerializationContext(topic2, MessageField.VALUE))
                    with Session(engine) as session:
                        query:Post=session.get(Post, dlete_cmt_event.post_id)
                        if not query:
                            print("Post not found")
                        else :
                            if query.comment_count==0:
                                ...
                            elif query.comment_count==1:
                                    query.commentcount=0
                            else:
                                query.comment_count-=1
                                session.add(query)
                                session.commit()    

                else :
                    print("No event found to deserilize  ok ...")
                  
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from consumer code in post service: {str(e)}"
        ) from e    
    finally:
        await consumer.stop()
        print("Consumer stopped.")

