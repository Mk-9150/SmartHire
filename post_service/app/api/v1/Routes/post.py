from fastapi import APIRouter , Depends , HTTPException,UploadFile,File,Header ,status,Path,Query , Form
from app.Models import post_model 
from typing import Union , Annotated,Any
import datetime
from app.crud.post import posti
from app.api.deps import session_Dep, tokenDep , kafka_producer , GET_TOKEN_Data
from aiokafka import AIOKafkaProducer , AIOKafkaConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient



router=APIRouter()







async def delivery_report(future):
    """
    Delivery report callback to handle success or failure of the produced message.
    """
    try:
        record_metadata = await future
        print(f"Message successfully delivered to {record_metadata.topic} [{record_metadata.partition}] at offset {record_metadata.offset}")
    except Exception as e:
        print(f"Failed to deliver message: {str(e)}")


  

    



  




@router.post("/createpost")
# async def createPostt(fale:UploadFile,user:GET_TOKEN_Data,timePlusTimezone:post_model.TimePlus_TimeZone  ,producer:kafka_producer , sesion:session_Dep):  
# async def createPostt(fale:UploadFile,timePlusTimezone:post_model.TimePlus_TimeZone_idk_why ,producer:kafka_producer , sesion:session_Dep)->Any:  
# async def createPostt(*,fale:UploadFile,user:GET_TOKEN_Data, timePlusTimezone:post_model.TimePlus_TimeZone_idk_why ,producer:kafka_producer , sesion:session_Dep)->Any:  
async def createPostt(*,fale:UploadFile,user:GET_TOKEN_Data, timezone:str=Query(alias="timezone")  ,localTime:str=Query(alias="localTime")  ,producer:kafka_producer , sesion:session_Dep):  
# async def createPostt(*,fale:UploadFile,producer:kafka_producer , sesion:session_Dep):  
    ...
    try:
        ...
        
        
        print(localTime)
        LocalTime_timeZone=post_model.UtcTime_timezone_Model(time_zone=timezone , utc_time=localTime)
        # print(LocalTime_timeZone.utc_time)   #  remeber this utc_time is represenying local times
        # return user
        return await posti.AddPost(user=user,sesion=sesion,timeDate_D=LocalTime_timeZone , fale=fale,producer=producer)          
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}" )  from e



# @router.post("/lastweekposts/{user_id}",response_model=post_model.PostReturn)
@router.post("/lastweekposts/{user_id}")
def get_last_week_posts(user_id:Annotated[int,Path()], timePlusTimezone:post_model.TimePlus_TimeZone, session:session_Dep):
    ...
    try:
        LocalTime_timeZone=post_model.UtcTime_timezone_Model(time_zone=timePlusTimezone.timezone , utc_time=timePlusTimezone.localTime)
        return posti.get_last_week_posts(username_id=user_id , timePlusTimezone=LocalTime_timeZone , session=session)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}" )  from e 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}" )  from e




@router.delete("/deletepost/{id}")
# async def postDeletion(id:Annotated[int,Path()],user:tokenDep, session:session_Dep, producer:kafka_producer ):
async def postDeletion(id:Annotated[int,Path()], session:session_Dep, producer:kafka_producer ):
    ...
    try:
        ...
        return await  posti.postDelete(id=id,session=session, producer=producer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}" )  from e  



router.get("/getpost/{id}")
def GetPostById(*,id:int=Path(),sesion:session_Dep):
    ...
    try:
        ...

        return  posti.Get_single_post(id=id,session=sesion) 


    except Exception as e:
      raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}" )  from e             
 


@router.get("/getposts/{userid}") 
def GetAllPosts(*,userid:int=Path(),session:session_Dep):
    ...
    try:
        ...
        return posti.Get_All_Postss(userid=userid, session=session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"{e}") from e    





