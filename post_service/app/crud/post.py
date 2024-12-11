from typing import Any
from sqlmodel import Session,select , and_ , or_
import uuid
import os
from sqlalchemy.orm import selectinload , joinedload ,Load , subqueryload , with_loader_criteria
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
import pytz
import datetime 

# NULL_OFFSET = -1



class PostCrud():
    
    
    
    async def postEvents(self,*,postid:int,userid:int,eventType:str="postCreated",producer:AIOKafkaProducer,topic:str,partition:int):
        ...
        schema_client=self.get_schema_registry_client()
        protobuff_serilizer=self.get_protobuf_serilizer(structure=postschema_pb2.PostCreated , schema_registry_cleint=schema_client)
    
        postData=postschema_pb2.PostCreated(event_type=eventType, post_id=postid, user_id=userid)
                    
        await self.produce_serilize_protobuf_messgae_to_kafka(producer=producer,topic=topic,protobuf_serializer=protobuff_serilizer,data=postData,partition=partition)
        
         
    
    def __convert_local_time_to_utc(self,*,user_timezone , localtime):
            ...
            try:
                ...
                    #  Parse the local time (string) into a datetime object
                # local_time = datetime.strptime(localtime, "%Y-%m-%d %H:%M:%S")  # Naive time

                #  Attach the timezone to make it timezone-aware
                local_timezone = pytz.timezone(user_timezone)
                local_time_with_tz = local_timezone.localize(localtime)  # Now it's timezone-aware

                #  Convert to UTC
                utc_time = local_time_with_tz.astimezone(pytz.utc)
                
                return utc_time
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")    
    
    
    
    def __convert_UTC_time_TO_LOCAL(self,user_timeZone , utc_time):
        ...
        try:
            ...
            # Step 1: Parse the UTC time (string) into a datetime object
            # utc_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S")  # Naive time
            utc_times = pytz.utc.localize(utc_time)  # Make it timezone-aware as UTC  ,  telling pytz  this is a Utc time 

            # Step 2: Convert UTC time to the specified local timezone
            local_timezone = pytz.timezone(user_timeZone) #  creating timezone obj
            
            local_time = utc_times.astimezone(local_timezone)  # Convert to local timezone  
            return local_time            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")    
    
    async def AddPost(self,*,user:Any,sesion:Session,timeDate_D:post_model.UtcTime_timezone_Model, fale,producer:AIOKafkaProducer):
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
                                
                            local_to_utc_time=self.__convert_local_time_to_utc(user_timezone=timeDate_D.time_zone, localtime=timeDate_D.utc_time)                     
                            timeModel=post_model.UtcTime_timezone(time_zone=timeDate_D.time_zone, utc_time=local_to_utc_time)
                            post=post_model.Post(Image_type=fileExt,pathIs=myPathIs,userid=user.id , haveTime=timeModel)  
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
                localTimeToUtc=self.__convert_local_time_to_utc(user_timezone=timeDate_D.time_zone, localtime=timeDate_D.utc_time)
                localTimeToUtc_Model=post_model.UtcTime_timezone(time_zone=timeDate_D.time_zone, utc_time=localTimeToUtc)               
                dataToBase=post_model.Post(Image_type=fileExt,pathIs=myPathIs,userid=user.id,haveTime=localTimeToUtc_Model)
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
            
            
            
    def __lastweek_Now(self, *, timePlusTimezone:post_model.UtcTime_timezone_Model):
        ...
        try:

            #1 first make time-zone aware   then  convert  time to the utc time  
            
            #2 tell pytz  about our timezone
            user_timezone = pytz.timezone(timePlusTimezone.time_zone)

            
        #   {
            
      #########     IMP  :   when you have naive  time  sooo you can   uncomment below line of code   that are in curly braces        
            #3  time  +  time-zone    now this will be time-zone aware  --->  finish ambiguity    
            #  this ->   timePlusTimezone.utc_time  is already  time zone aware  sooo that is why below line is commented    ,  if you have naive time   soo you can uncomment delow line
            # userTime_with_tz=user_timezone.localize(timePlusTimezone.utc_time) #  this timePluszone.utc_time is representing local_time  
              #4  utc  conversion
            # utc_time= userTime_with_tz.astimezone(pytz.utc)
           
        #   } 
        
        # {
            # i had time zone aware  obj  soo  i directly  convert it to  utcimes
            utc_time=timePlusTimezone.utc_time.astimezone(pytz.utc)
            
        # }   
            # 5 Now calculate the time 7 days ago in UTC
            seven_days_ago_utc = utc_time - datetime.timedelta(days=7)
            return seven_days_ago_utc , utc_time            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")            
            
            
    def get_last_week_posts(self,*,username_id:int ,timePlusTimezone:post_model.UtcTime_timezone_Model ,  session:Session):
        try:
            ...
            
            # print("helloooooooooooooooooooooooooooo====================")
            
            # First get seven_days_ago_utc and utc_now
            seven_days_ago_utc, utc_now=self.__lastweek_Now(timePlusTimezone=timePlusTimezone)
            print(seven_days_ago_utc , utc_now)
            # print("helloooooooooooooooooooooooooooo====================")
            
                                                                # with_loader_criteria(post_model.UtcTime_timezone, lambda utcTime: utcTime.utc_time >= seven_days_ago_utc and utcTime.utc_time <= utc_now) 
            postsFromUser:post_model.Post=session.exec(select(post_model.Post)
                                                       .options(joinedload(post_model.Post.haveTime) ,
                                                                with_loader_criteria(post_model.UtcTime_timezone,
                                                                                     or_(post_model.UtcTime_timezone.utc_time >= seven_days_ago_utc , post_model.UtcTime_timezone.utc_time <= utc_now)), 
                                                                Load(post_model.Post).raiseload("*"))
                                                       .where(post_model.Post.userid==username_id)).unique().all()
            
            
        
            if not postsFromUser:
                # print("Kuch ni Mila hehehehehhehehehhhhheeheh")
                return status.HTTP_404_NOT_FOUND
            
            # ReturningData:dict[str,dict[str,Any]]={}
            
            
            # for s_post in postsFromUser:
            #     s_post.haveTime.utc_time=self.__convert_UTC_time_TO_LOCAL(user_timeZone=timePlusTimezone.time_zone, utc_time=s_post.haveTime.utc_time)
            #     print(s_post.haveTime.utc_time) 
            #     ReturningData[f"0{s_post.id}"]=s_post.model_dump()
            #     ReturningData[f"0{s_post.id}"]["haveTime"]=s_post.haveTime.model_dump()
                
                
            # return ReturningData
            
            return postsFromUser
          
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")  from e  
        
        
        
          
                
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