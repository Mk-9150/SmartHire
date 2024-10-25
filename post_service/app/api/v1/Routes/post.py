from fastapi import APIRouter , Depends , HTTPException,UploadFile,File,Header ,status,Path,Query
from app.Models import post_model 
from typing import Union , Annotated,Any
from app.crud.post import posti
from app.api.deps import session_Dep, tokenDep , kafka_producer
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


  

    


# @router.get("/testdata")
  




@router.post("/createpost")
async def createPostt(fale:UploadFile,user:tokenDep,producer:kafka_producer ,sesion:session_Dep)->post_model.PostReturn:  
    ...
    try:
        ...
        return await posti.AddPost(user=user,sesion=sesion,fale=fale,producer=producer)          
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





