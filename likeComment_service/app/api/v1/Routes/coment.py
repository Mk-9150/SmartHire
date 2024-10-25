from fastapi import APIRouter , Depends , HTTPException , status , Path , Query
from aiokafka import AIOKafkaProducer 
from app.models import comment_model
from app.api.deps import SessionDependency,  L_producer
from app.crud.comments import cmt

server=APIRouter()


@server.get("/allcmt")
def get_all_comments():
    ...    



@server.post("/addcmt")
async def add_comment(data:comment_model.Comment_DataReceived , session :SessionDependency ,producer:L_producer):
    ...
    try:
        ...  
        await cmt.post_comment(data=data,sesison=session,producer=producer)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Unxpected Erorr occurs{e}"))    from e    


@server.delete("/delcmt/{post_id}")
async def deleted_commet(*,post_id:int=Path() , comment_by:str=Query(alias="comentby") , session:SessionDependency , producer:L_producer ):
    ...
    try:
        ...
        await cmt.delete_comment(post_id=post_id, comment_by=comment_by, session=session, producer=producer)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e    