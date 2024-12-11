from fastapi import HTTPException , status ,APIRouter , Path  , BackgroundTasks 
from app.api.deps import GET_SESSION
from app.api.deps import GET_TOKEN_DATA
from app.crud.RelationsCrud import userRelation
from app.models import time_timezone_model 
from app.crud.UsersFeed import feedu


connect=APIRouter()


# *=======>     IMPORTTANT  The ids  at path operation are  Actualuser_ids    ,  not  refering to id (pk)

@connect.post("/followto/{id}")
def follow(*,id:int=Path() ,token:GET_TOKEN_DATA ,time_timezone:time_timezone_model.LocalTimePlus_imeTimeZone ,backGround_Task:BackgroundTasks,  session:GET_SESSION): 
    ...
    try:
        #  return token
         userRelation.followTO(own_id=token.id, folloeTo_id=id ,  username=token.username , session=session)          
         jsonSerilized_Time_timezone_Obj=time_timezone_model.LocalTimePlus_imeTimeZone_create(**time_timezone.model_dump())  
         backGround_Task.add_task(feedu.get_lastWeek_posts(Actual_User=token.id,followedUser_user_id=id,time_timeZone=jsonSerilized_Time_timezone_Obj ,session=session));
        #  return feedu.get_lastWeek_posts(Actual_User=token.id,followedUser_user_id=id,time_timeZone=jsonSerilized_Time_timezone_Obj ,session=session)
                 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from follow in Feed service: {str(e)}"	
        ) from e    



@connect.post("/followback/{id}")    # this id must be follow back person id 
def Follow_Back(*,id:int=Path(description="the id of the follow back user",),time_timeZone:time_timezone_model.LocalTimePlus_imeTimeZone,backGround:BackgroundTasks , token:GET_TOKEN_DATA,session:GET_SESSION ):
    try:
        ...
        
        data=userRelation.FollowBack(own_id=token.id, followBack_User_id=id,session=session)
        
        JsonSerilized_Time_TimeZone=time_timezone_model.LocalTimePlus_imeTimeZone_create(**time_timeZone.model_dump())
        backGround.add_task(feedu.get_lastWeek_posts(Actual_User=token.id, followedUser_user_id=id, time_timeZone=JsonSerilized_Time_TimeZone, session=session))
        return status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from follow back in Feed service: {str(e)}"
        ) from e    

@connect.post("/unfollow/{id}")
def unfollow(*, id:int=Path(description="the id of the unfollow user"), token:GET_TOKEN_DATA, session:GET_SESSION, backGRounD:BackgroundTasks):
    ...
    try:
        ...
        
        return  userRelation.UnFollow_User(own_id=token.id, unfollow_userId=id, background=backGRounD , session=session)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from unfollow in Feed service: {str(e)}"
        ) from e
        
        
        
@connect.get("/search/{username}") 
def search(*, username:str=Path(description="the username of the user"),session:GET_SESSION):
  try:
      ...
      user=userRelation.searchUser(username=username, session=session)
  except HTTPException as e:
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Error from search in Feed service: {str(e.detail)}"
      ) from e
      
  except Exception as e:
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Error from search in Feed service: {str(e)}"
      ) from e            
