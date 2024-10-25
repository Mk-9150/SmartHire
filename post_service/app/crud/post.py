from typing import Any
from sqlmodel import Session,select
import uuid
import os
from fastapi import HTTPException , status, Depends
from app.Models import post_model
# from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from app.service_schema import structure_pb2
from confluent_kafka.serialization import SerializationContext ,MessageField
from uuid import uuid4
from aiokafka import AIOKafkaProducer
from app.core.app_settings import setting
from typing import Annotated
from app.service_schema import postschema_pb2

# NULL_OFFSET = -1



class PostCrud():
    
    async def postEvents(self,*,postid:int,userid:int,eventType:str="postCreated",producer:AIOKafkaProducer,topic:str,partition:int):
        ...
        schema_client=self.get_schema_registry_client()
        protobuff_serilizer=self.get_protobuf_serilizer(structure=postschema_pb2.PostCreated , schema_registry_cleint=schema_client)
    
        postData=postschema_pb2.PostCreated(event_type=eventType, post_id=postid, user_id=userid)
                    
        await self.produce_serilize_protobuf_messgae_to_kafka(producer=producer,topic=topic,protobuf_serializer=protobuff_serilizer,data=postData,partition=partition)
        
         
        

    async def AddPost(self,*,user:Any,sesion:Session,fale,producer:AIOKafkaProducer):
        try:
          if user.username:
            username=user.username
            

            images_type=["jpg","png","jpeg"]
            
            if fale and isinstance(fale.content_type,str):

                filename = f"{uuid.uuid4()}.{fale.content_type.split('/')[1]}"
                fileExt=filename.split(".")[-1].lower()
                
                if fileExt in images_type:
                    pathIs="app/usersPost/images/"
                    newDirectory= username
                    pathIs=os.path.join(pathIs, newDirectory)
                    
                try:

                    os.makedirs(pathIs)
                    # return "Directory Created"
                except FileExistsError as e:
                        print("Directory already exist")
                        myPathIs=os.path.join(pathIs, filename)
                        
                        try:
                            with open(myPathIs, "wb") as f:
                                f.write(await fale.read())
                            
                            post=post_model.Post(Image_type=fileExt,pathIs=myPathIs,userid=user.id)                               
                            
                            sesion.add(post)
                            sesion.commit()
                            sesion.refresh(post)
                            # code for Event creation to kafka brokers 
                            returnedResponse=await self.postEvents(postid=post.id, userid=user.id,  producer=producer,  topic=setting.KAFKA_TOPIC_NAME,partition=0)
                            
                            return post
                        except FileExistsError:
                            return "not written "  
                except Exception as e:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
                
                myPathIs=os.path.join(pathIs, filename)
                dataToBase=post_model.Post(Image_type=fileExt,pathIs=myPathIs,userid=user.id)
# 
                try:                
                    with open(myPathIs, "wb") as f:
                        f.write(await fale.read())
                    sesion.add(dataToBase)
                    sesion.commit()
                    sesion.refresh(dataToBase)
                    returnedResponse=await self.postEvents(postid=dataToBase.id, userid=user.id,  producer=producer,  topic=setting.KAFKA_TOPIC_NAME,partition=0)
                    print(returnedResponse)
                    return dataToBase
                
                except FileExistsError:
                    return "not written " 
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}" )  from e
            
                
    # async  def postDelete(self,*,id:int,session:Session,user:Any,producer:AIOKafkaProducer):
    async  def postDelete(self,*,id:int,session:Session,producer:AIOKafkaProducer):
        ...
        try:
                       
                postData=session.get(post_model.Post,id)
                if not postData :
                    raise HTTPException(status_code=404, detail="Post not found")
                session.delete(postData)
                session.commit()
                
                await self.postEvents(postid=postData.id, userid=2, eventType="postDeleted", producer=producer, topic=setting.KAFKA_TOPIC_NAME2, partition=1)
                return "Post deleted"
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}" )  from e
        


    def Get_single_post(self,*,id:int,session:Session):
        ...
        try:
            ...
            
            post_data=session.get(post_model.Post,id)

            if not post_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")

            return post_data 
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"{e}") from e    

    def Get_All_Postss(self,*,userid:int , session:Session):
        ...
        try:
            ...
            # posts=session.query(post_model.Post).filter(post_model.Post.userid==userid).all()
            posts= session.exec(select(post_model.Post).where(post_model.Post.userid==userid)).all()
            if not posts:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            return posts
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e} some un expected happens to your server") from e    
    


    def get_schema_registry_client(self):
        ...
        try:
             schema_registry_client = SchemaRegistryClient({"url": setting.SCHEMA_REGISTRY_URL})
             return schema_registry_client
        except Exception as e:
             raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}" )  from e    
    
    
    # async def get_kafka_producer(server_url:str):

                    
    async def produce_serilize_protobuf_messgae_to_kafka(self,*,producer:AIOKafkaProducer , topic:str,protobuf_serializer,data,partition:int):
        ...
        """
        Produces a Protobuf message asynchronously to a Kafka topic.
        """
        try:
            payload = protobuf_serializer(data, SerializationContext(topic, MessageField.VALUE))
           
            # future = await producer.send_and_wait(topic, key=str(uuid4()).encode('utf-8'), value=payload)
            await producer.send_and_wait(topic, key=str(uuid4()).encode('utf-8'), value=payload,partition=partition)
            return "event sent to kafka broker"
            # await delivery_report(future)
        except Exception as e:
            print(f"Error producing message: {str(e)}")
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}" )  from e
            # return NULL_OFFSET
        # return future.offset  
        
    def get_protobuf_serilizer(self,*,structure, schema_registry_cleint:SchemaRegistryClient):
        ...
        try:
            
            protobuf_serializer = ProtobufSerializer(structure, schema_registry_cleint, {"use.deprecated.format": False})
            return protobuf_serializer
        except Exception as e:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e} : eror at get protobuf serilizer  " )  from e    
            
            
    
            
        
    # async def testing_purpose(self,producer:Annotated[AIOKafkaProducer,Depends(get_kafka_producer)]):
        ...
        # try:
            # ...
            # person = structure_pb2.Person(id=1,name="shani ")
            
            # await self.produce_serilize_protobuf_messgae_to_kafka(producer, setting.KAFKA_TOPIC_NAME, protobuf_serializer, person)
            


        # except Exception as e:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail=f"{e}" )  from e         
            
                
posti=PostCrud()                