from fastapi import HTTPException , status 
from app.api.deps import GET_SESSION
from sqlmodel import Session , select
import requests
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm import joinedload , Load , selectinload 
from app.models import Relationship_model 
from app.core.app_setting import  setting
from typing  import Optional , Annotated , List , Literal , Union
from app.models import time_timezone_model  
class FeedCrud():
    ...
      #  followedUser_user_id  ->  this parameter will be Actualuser_id   not id(* primary key )
    def get_lastWeek_posts(self,*,Actual_User:int , followedUser_user_id:int, time_timeZone:time_timezone_model.LocalTimePlus_imeTimeZone_create ,session:Session):
        ...
        try:
            ...
            url:str=f"{setting.POST_SERVICE_URL}/api/v1/posts/lastweekposts/{followedUser_user_id}"
            Time_timeZone_Data_dict:dict=time_timeZone.model_dump()
                # 'Authorization': f'Bearer {setting.POST_SERVICE_TOKEN}',  # Include the token in the Authorization header
            headers = {
                'Content-Type': 'application/json'   # Set the content type, typically 'application/json'
            }
            response=requests.post(url=url,json=Time_timeZone_Data_dict,headers=headers)
            print(response.status_code)
            if response.status_code==200:
                print("Request was successful!")
                data= response.json()
                Actual_User_data:Relationship_model.User=session.exec(
                    select(Relationship_model.User)
                    .options(joinedload(Relationship_model.User.haveFeed),
                            Load(Relationship_model.User).raiseload("*")
                            )
                    .where(Relationship_model.User.Actualuser_id==Actual_User)
                ).unique().one_or_none()
                
                if not Actual_User_data:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found  at Feed Service")
                # return data
                List_postIds:list[int]=list(map(lambda x: x.get("id") , data))
                # return List_postIds
                if  not Actual_User_data.haveFeed:
                    feedModel=Relationship_model.Userfeed(feed=list(set(List_postIds)))
                    Actual_User_data.haveFeed=feedModel
                    session.add(Actual_User_data)
                    session.commit()
                    return status.HTTP_200_OK
                Actual_User_data.haveFeed.feed.extend(List_postIds)
                flag_modified(Actual_User_data.haveFeed, "feed")
                session.add(Actual_User_data)
                session.commit()
                return status.HTTP_200_OK
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"{e}")   from e 
            
    
    
    # def __removeIds_from_UserFeed(self, *, Actual_User:int | None=None, unfollowedUser_user_id:Optional[int]=None, listofIds:list[int]|dict[str,list[int]] ,session:Session):
    def __removeIds_from_UserFeed(self, *, Actual_User:int | None=None, listofIds:list[int]|dict[str,list[int]] ,session:Session):
        ...
        try:
            ...
            if isinstance(listofIds, list):
                ...
                if listofIds:
                        if Actual_User :
                            Actual_User_data:Relationship_model.User=session.exec(
                                select(Relationship_model.User)
                                .options(joinedload(Relationship_model.User.haveFeed),
                                        Load(Relationship_model.User).raiseload("*")
                                        )
                                .where(Relationship_model.User.Actualuser_id==Actual_User)
                            ).unique().one_or_none()

                            if not Actual_User_data:
                                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found  at Feed Service")
                            # return data
                            if not Actual_User_data.haveFeed:
                                return {"status":status.HTTP_200_OK , "message":"No Feed to remove, User have no feed"}

                            else :
                                Actual_User_data.haveFeed.feed=list(set(Actual_User_data.haveFeed.feed)-set(listofIds))
                                flag_modified(Actual_User_data.haveFeed, "feed")
                                session.add(Actual_User_data)
                                session.commit()
                                return {"status":status.HTTP_200_OK , "message":"Feed removed successfully"}
                        
            else :
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"listofIds must be a list in USERFEED_PY")

        except HTTPException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{e}")   from e     
            
        except  Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{e}")   from e    
            
            
    def __make_Requests(self,*,id:int):
        ...
        url:str=f"{setting.POST_SERVICE_URL}/api/v1/posts/getposts/{id}"
        headers = {
            'Content-Type': 'application/json'   # Set the content type, typically 'application/json'
        }
        resonse=requests.get(url=url, headers=headers)
        return resonse
        # if resonse.status_code==200:
        #     print("Request was successful!")
        #     data= resonse.json()
        #     return data
        
        # else :
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=f"Request to post service failed")    
            
            
            
         
    
    def getAllPostIDS_And_removeUpdateFEED_2(self,*,actual_userid:Union[int,None]=None,unfollowedUser_id:int|None=None , session:Session):
        try:
           ...
           if actual_userid is None and unfollowedUser_id is None:
               raise HTTPException(
                   status_code=status.HTTP_400_BAD_REQUEST,
                   detail=f" actual_userid and unfollowedUser_id must be provided")
           elif actual_userid and not unfollowedUser_id:
               raise HTTPException(
                   status_code=status.HTTP_400_BAD_REQUEST,
                   detail="actual_userid is Given  but also provide unfollowedUser_id "
               )    
           elif unfollowedUser_id and not actual_userid:
               raise HTTPException(
                   status_code=status.HTTP_400_BAD_REQUEST,
                   detail="unfollowedUser_id is Given  but also provide actual_userid "
               )
           else :
               ...
               response = self.__make_Requests(id=unfollowedUser_id)
               if response.status_code == 200:
                   data = response.json()
                   list_of_postIDS = list(map(lambda x: x.get("id"), data))
                   self.__removeIds_from_UserFeed(Actual_User=actual_userid,listofIds=list_of_postIDS,session=session)
                   return {"status": status.HTTP_200_OK, "message": "Feed removed successfully"}
               else:
                   raise HTTPException(
                       status_code=status.HTTP_400_BAD_REQUEST,
                       detail=f"Request to post service failed")
                   
        except  HTTPException as e:
            raise HTTPException (
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{e}")   from e    
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{e}")   from e
feedu=FeedCrud()

    