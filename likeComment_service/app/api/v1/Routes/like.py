from fastapi import HTTPException , status , APIRouter , Depends , Path
from app.models import like_mode
from app.api.deps import SessionDependency,  L_producer 
from app.crud.like import lke

router=APIRouter()



@router.post("/liked")
async def likedpost(*, data:like_mode.receiveData, session:SessionDependency,producer:L_producer):
    ...
    try:
        ...
        await lke.postLike(like=data, session=session,producer=producer)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e

@router.get("/postid")
def get_all_likes_of_post(*,postid:int=Path() ,data:like_mode.receiveData ,session:SessionDependency ):
    ...
    try:
        ... 
        # lke.postLike(like=like_mode.Like(**data.dict()),session=session)
        lke.postLike(like=data,session=session)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))    from e
    # return {"message":"all comments"}
    
    
@router.post("/dislike")
async def postUnliked(data:like_mode.unlikeData , session:SessionDependency , producer:L_producer):
    ...
    try:
        ...
        await   lke.postUnlike(postid=data.post_id, dislikeBy=data.un_likedBy, session=session, producer=producer  )
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    from e    