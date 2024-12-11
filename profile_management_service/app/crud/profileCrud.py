from fastapi import HTTPException , Depends , status

from sqlmodel import Session,select
from sqlalchemy import and_
from sqlalchemy.orm import selectinload , joinedload 
from app.models import teacher_model
from app.models import teacher_model





class ProfileCrud():
    
    
    # def chkUserExistsorNot(self,*,id:int,username:str):
    #     ...
    #     url="http://localhost:8002/currentuser"  #  the URL For user management service to get current user
    #     headers = {
    #         'Authorization': f'Bearer {token}',  # Include the token in the Authorization header
    #         'Content-Type': 'application/json'   # Set the content type, typically 'application/json'
    #      }
                
    
    def get_profile(self, user: str , session:Session):
        
        try:
            profile = session.exec(selectinload(teacher_model.Teacher).where(teacher_model.Teacher.username==user)).one_or_none()
            # profile = session.exec(select(teacher_model.Teacher).where(teacher_model.Teacher.username==user)).one_or_none()
            if not profile:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Profile with name {user} not found")
            return profile
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Something went wrong")
        
        
        
        
    def create_profile(self,username:str, teacher:teacher_model.TeachrCreate, session:Session ):
        
        try:
            
            teacher.username=username            
            NewTeacher:teacher_model.Teacher = teacher_model.Teacher.model_validate(teacher)
            session.add(NewTeacher)
            session.commit()
            session.refresh(NewTeacher)
            return NewTeacher
            
            
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Something went wrong")
        
        
       
     

    def update_profile(self, user_id: int, profile_update: teacher_model.UpdateModel , session:Session):
      
      try:
          
        profile_to_update = session.get(teacher_model.Teacher, user_id)
        if not profile_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Profile with id {user_id} not found")
        
        profile_data=profile_update.model_dump(exclude_unset=True)
        
        profile_to_update.sqlmodel_update(profile_data)
        session.add(profile_to_update)
        session.commit()
        session.refresh(profile_to_update)        
        return profile_to_update
      except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Something went wrong")




    



techer=ProfileCrud()    