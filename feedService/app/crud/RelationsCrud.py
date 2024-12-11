from fastapi  import HTTPException , status
from sqlmodel import Session , select , and_ 
from sqlalchemy.orm import selectinload  , joinedload
from sqlalchemy.orm.attributes  import flag_modified
from app.models import Relationship_model
from sqlalchemy.orm import Load
from fastapi  import BackgroundTasks
from app.crud.UsersFeed import feedu
class RelationsCrud():
    ...
    def followTO(self,* , own_id:int , folloeTo_id:int , username:str , session:Session  ):
            try:
                ...
     #  {  the code in curly brakets  can be fetched once  i mean  you dont need to query seperately , it is not required , 
    #      How ?
    #      you can just override where cond. to below line  
    #      where(and_(Relationship_model.User.id.in_([own_id,followBack_User_id]) ) ) 
                
                user:Relationship_model.User=session.exec(
                    select(Relationship_model.User)
                    .options(joinedload(Relationship_model.User.haveRelation)
                            ,joinedload(Relationship_model.User.haveFeed))
                    .execution_options(populate_existing=True)
                    .where(Relationship_model.User.Actualuser_id==own_id)
                    ).unique().one_or_none()
                if not user :
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found  at Feed Service")
                
                # return user
            #  Remember  if you overide the where cond. of first query to above line with and_() cond. inside  
            # then the below code should be commented to removed because it will be fetched in above query 
                followToUser:Relationship_model.User=session.exec(
                select(Relationship_model.User)
                .options(joinedload(Relationship_model.User.haveRelation)
                            ,joinedload(Relationship_model.User.haveFeed)).
                execution_options(populate_existing=True)
                .where(Relationship_model.User.Actualuser_id==folloeTo_id)).unique().one_or_none()
    #    }
                if not followToUser :
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="follow to User not found  at Feed Service")
                
                # return   followToUser
                
                if followToUser and user  and  not followToUser.haveRelation and not user.haveRelation:
                    print("1")
                    followToRelation:Relationship_model.UserRelationship=Relationship_model.UserRelationship(followed_by=[(user.Actualuser_id,user.username)],follow_back=[(user.Actualuser_id,user.username)])
                    followToUser.haveRelation=followToRelation
                    ownUser=Relationship_model.UserRelationship(following=[(followToUser.Actualuser_id,followToUser.username)] )
                    user.haveRelation=ownUser
                    session.add_all([followToUser, user])
                    session.commit()
                    return 
                
                if user and user.haveRelation and not followToUser.haveRelation:
                    print("2")
                    followToRelation:Relationship_model.UserRelationship=Relationship_model.UserRelationship(followed_by=[(user.Actualuser_id, user.username)], follow_back=[(user.Actualuser_id, user.username)])
                    user.haveRelation.following.append((followToUser.Actualuser_id, followToUser.username))
                    followToUser.haveRelation=followToRelation
                    
                    flag_modified(user.haveRelation, "following")
                    
                    session.add_all([followToUser, user])
                    session.commit()
                    return user.haveRelation
                
                if followToUser and followToUser.haveRelation and not user.haveRelation:
                    print("3")
                    ActualUser_Relation_model:Relationship_model.UserRelationship=Relationship_model.UserRelationship(following=[(followToUser.Actualuser_id, followToUser.username)])
                    followToUser.haveRelation.follow_back.append((user.Actualuser_id, user.username))
                    followToUser.haveRelation.followed_by.append((user.Actualuser_id, user.username))        
                    
                    user.haveRelation=ActualUser_Relation_model
                    flag_modified(followToUser.haveRelation, "followed_by")
                    flag_modified(followToUser.haveRelation, "follow_back")
                    session.add_all([followToUser, user])
                    session.commit()
                    return followToUser.haveRelation
                    ##    Push notification of follow Back 
                
                
                
                if followToUser and followToUser.haveRelation  and user and user.haveRelation:    
                    print("4")
                    # print(followToUser.haveRelation)
                    followToUser.haveRelation.followed_by.append((user.Actualuser_id, user.username))    
                    followToUser.haveRelation.follow_back.append((user.Actualuser_id, user.username))
                    user.haveRelation.following.append((followToUser.Actualuser_id, followToUser.username))
                    
                    flag_modified(followToUser.haveRelation, "followed_by")
                    flag_modified(followToUser.haveRelation, "follow_back")
                    flag_modified(user.haveRelation, "following")
                    
                    session.add_all([followToUser, user])
                    session.commit()
                    session.refresh(user)
                    session.refresh(followToUser)
                    return {"ftu":followToUser.haveRelation , "ac":user.haveRelation}
            
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}") from e    
    
        
        
    def FollowBack(self,* ,own_id:int, followBack_User_id:int,  session:Session):
            try:
                ...
    #  {  the code in curly brakets  can be fetched once  i mean  you dont need to query seperately , it is not required , 
    #     How ?
    #     you can just override where cond. to below line  
    #     where(Relationship_model.User.Actualuser_id.in_([own_id,followBack_User_id]) ) 
                ActualUser:Relationship_model.User=session.exec(
                    select(Relationship_model.User)
                    .options(joinedload(Relationship_model.User.haveRelation)
                             ,joinedload(Relationship_model.User.haveFeed)).
                    execution_options(populate_existing=True)
                    .where(Relationship_model.User.Actualuser_id==own_id)
                ).unique().one_or_none()
                
                
                if not ActualUser:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found  at Feed Service")
                
                FollowBacked_User:Relationship_model.User=session.exec(
                    select(Relationship_model.User)
                    .options(joinedload(Relationship_model.User.haveRelation)
                             ,joinedload(Relationship_model.User.haveFeed)).
                    execution_options(populate_existing=True)
                    .where(Relationship_model.User.Actualuser_id==followBack_User_id)
                ).unique().one_or_none()
    #   }   
                
                if not FollowBacked_User:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="follow to User not found  at Feed Service")
                
                
                
                
                #  Now remove user from ActualUser follow_back  field   ,  who actually follows back to user 
                #   removing the user from followback field of Actual user  bevause he followed back
                Removed_User_From_FollowBack_of_ActualuSER = list(filter(lambda x: x[0] != FollowBacked_User.Actualuser_id, ActualUser.haveRelation.follow_back))
                
                ActualUser.haveRelation.follow_back=Removed_User_From_FollowBack_of_ActualuSER
                
                # Now  also adds  FollowBacked_User  followed_by field  the id and username of Actual user who follows back 
                RelationModel_for_FollowBacked_User:Relationship_model.UserRelationship=Relationship_model.UserRelationship(followed_by=[(ActualUser.Actualuser_id, ActualUser.username)])
                
                
                #  removing the relationship from following Field of Followedback user  beacaUSE  the Atcul user followed back 
                # soo now   actual user is a follower of followed back user  
                # and it must important to remove relation of following field  in the folloedback user
                Remove_Relation_from_followBacked_User_in_following_field = list(filter(lambda x: x[0] != ActualUser.Actualuser_id, FollowBacked_User.haveRelation.following))
                FollowBacked_User.haveRelation.following=Remove_Relation_from_followBacked_User_in_following_field
                FollowBacked_User.haveRelation.followed_by.append((ActualUser.Actualuser_id, ActualUser.username))
                
                flag_modified(FollowBacked_User.haveRelation, "followed_by")

                session.add_all([ActualUser, FollowBacked_User])
                session.commit()
                session.refresh(ActualUser)
                session.refresh(FollowBacked_User)
                
                
                #    Push Notification   code    ...       
                
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}") from e    
    
    
    
    def UnFollow_User(self, *,own_id:int,unfollow_userId:int,background:BackgroundTasks,  session:Session):
        ...
        try:
            ...
            Users:list[Relationship_model.User]=session.exec(
                select(Relationship_model.User)
                .options(joinedload(Relationship_model.User.haveRelation)
                         ,joinedload(Relationship_model.User.haveFeed),Load(Relationship_model.User).raiseload("*")).
                where(Relationship_model.User.Actualuser_id.in_([own_id,unfollow_userId]))
                ).unique().all() 
            # Users:list[Relationship_model.User]=session.exec(
            #     select(Relationship_model.User)
            #     .options(joinedload(Relationship_model.User.haveRelation)
            #              ,joinedload(Relationship_model.User.haveFeed)).
            #     where(Relationship_model.User.Actualuser_id==own_id)
            #     ).unique().all() 
            
            # return Users
            
            if not Users:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found  at Feed Service")
            
            ActualUser:Relationship_model.User=  Users[0] if Users[0].Actualuser_id ==own_id  else  Users[1]
            if not ActualUser:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found  at Feed Service")
            
            unfollowedUser:Relationship_model.User=Users[0] if Users[0].Actualuser_id ==unfollow_userId  else  Users[1]
            if not unfollowedUser:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="follow to User not found  at Feed Service")
            
            
            #  first chk in  followby  field of Actual user  if unfollowed user is present or not
            #  if present then remove it
            
            # below line of code is the unfollowed user id in the list   e.g [34]
            unfollowedUser_is_follower_of_actualUser=list(filter(lambda x: x[0] == unfollowedUser.Actualuser_id, ActualUser.haveRelation.followed_by))
            
            # if unfollowedUser_is_follower_of_actualUser:
            #     ActualUser.haveRelation.followed_by=list(filter(lambda x: x[0] != unfollowedUser.Actualuser_id, ActualUser.haveRelation.followed_by))
             
             
             
            # Does Actual user follower Of unfollowedUser  ?
            Check_ActualUser_is_follower_of_unfollowedUser=list(filter(lambda x: x[0] == ActualUser.Actualuser_id, unfollowedUser.haveRelation.followed_by))
            if  unfollowedUser_is_follower_of_actualUser  and Check_ActualUser_is_follower_of_unfollowedUser:
                # ActualUser.haveRelation.followed_by=list(filter(lambda x: x[0] != unfollowedUser.Actualuser_id, ActualUser.haveRelation.followed_by))
                 
                ActualUser.haveRelation.follow_back.append((unfollowedUser.Actualuser_id, unfollowedUser.username))
                unfollowedUser.haveRelation.followed_by=list(filter(lambda x: x[0] != ActualUser.Actualuser_id, unfollowedUser.haveRelation.followed_by)) 
                
                unfollowedUser.haveRelation.following.append((ActualUser.Actualuser_id, ActualUser.username))
                
                flag_modified(unfollowedUser.haveRelation, "following") 
                flag_modified(ActualUser.haveRelation, "follow_back") 
            
                session.add_all([ActualUser, unfollowedUser])
                session.commit()
                
                # here reomve the ids from both users feed 
                #  how ?
                #   update the feed of actual user  who unfollowed the user   , get the post ids of unfollowed user and remove the post ids from actual user feed
                background.add_task(feedu.getAllPostIDS_And_removeUpdateFEED_2(actual_userid=ActualUser.Actualuser_id, unfollowedUser_id=unfollowedUser.Actualuser_id, session=session))
                return "Success  unfollow"
            

            # Now chk    unfollowed user is in the Actual user  followings  
            # if present then the list will looks like   [32]  * 32 is dummy here  i mean the actualuser_id  will be in the list *
            unFollowedUser_in_Actualuser_Following=list(filter(lambda x: x[0] == unfollowedUser.Actualuser_id, ActualUser.haveRelation.following))
            if  unFollowedUser_in_Actualuser_Following:
                # unfollowedUser.haveRelation.following=list(filter(lambda x: x[0] != ActualUser.Actualuser_id, unfollowedUser.haveRelation.following)) unfollowedUser_is_follower_of_actualUser:
                ActualUser.haveRelation.following=list(filter(lambda x: x[0] != unfollowedUser.Actualuser_id, ActualUser.haveRelation.following))
                unfollowedUser.haveRelation.followed_by=list(filter(lambda x: x[0] != ActualUser.Actualuser_id, unfollowedUser.haveRelation.followed_by))                         
                unfollowedUser.haveRelation.follow_back=list(filter(lambda x: x[0] != ActualUser.Actualuser_id, unfollowedUser.haveRelation.follow_back))
                session.add_all([ActualUser, unfollowedUser])
                session.commit()
                session.refresh(ActualUser)
                background.add_task(feedu.getAllPostIDS_And_removeUpdateFEED_2(actual_userid=ActualUser.Actualuser_id,unfollowedUser_id=unfollowedUser.Actualuser_id, session=session))
                return "Unfollowed"
            
                # here  i removed the post ids from the feed of actual user  who unfollowed the user
            
            # return "Already unfollowed"
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}") from e
    
    
    def searchUser(self, *, username:str, session:Session):
        try:
            ...
            user:Relationship_model.User=session.exec(
                select(Relationship_model.User)
                .options(joinedload(Relationship_model.User.haveRelation)
                        #  ,joinedload(Relationship_model.User.haveFeed)).
                ).where(Relationship_model.User.username==username)
                ).unique().one_or_none()
            
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found  at Feed Service")
            
            if not user.haveRelation:
                return   { "user" :user , "value":False }  #  False means user is not followed by anyone

            return { "user" :user ,"followers":user.haveRelation.followed_by , "following":user.haveRelation.following,"value":True } 
            
            # return user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}") from e
    
userRelation=RelationsCrud()    