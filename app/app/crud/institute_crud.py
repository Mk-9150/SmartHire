from typing import Any 
from fastapi import Depends , status , HTTPException 
from app.models.Institute_model import InstituteCreate , Institute
from sqlmodel import Session ,select
from app.core.loggerConfig import loggeng
from app.core.settings import setting
from datetime import timedelta
from app.core.security import verify_password , get_hashed_Password , createToken

logger=loggeng(__name__)



class InstituteCrud():

    def usernameExist(self,*,username:str,session:Session):
        
        instute:Institute=session.exec(select(Institute).where(Institute.name==username)).one_or_none()
        return instute if  instute else False 
        # if not instute:
        #     return True 
        # return False 
        ...
    
    def EmailExist(self,*,emial:str,sesion:Session):
        
        institute:Institute=sesion.exec(select(Institute).where(Institute.email==emial)).one_or_none()
        
        return True if not institute else False
        
        ...
    

    def createInstitutes(self,*,institute_Create:InstituteCreate ,session:Session):
        
        try:
            #  *check -> if the username exist or Email Exist  already 
            
            if isinstance(self.usernameExist(username=institute_Create.name,session=session),Institute):
                raise HTTPException (
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username Aready Exist !"
                )
                
            if isinstance(self.EmailExist(emial=institute_Create.email , sesion= session),Institute):
                 raise HTTPException (
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email Aready Exist !  PLease  Use another "
                )             
            
            institute_:Institute=Institute.model_validate(
                institute_Create,update={"hashed_password":get_hashed_Password(institute_Create.password) }
            )
                       
            session.add(institute_)
            session.commit()
            realInstitute:Institute=session.refresh(institute_)
            
            #Create Acces Token for user for authorization , authentication
            expires=setting.TOKEN_EXPIRES_TIME
            print(expires)
            
            return createToken(data={"id":institute_.id,"username":institute_.name},expires=timedelta(days=1))
            
            
            # return {"created":"Your Account created SuccessFully"}                
        
        except HTTPException as e:
            
            logger.error(e)
        
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{e}"
                ) from e     
        
        except Exception as e:
            logger.error(e)
            raise HTTPException (
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error ! Unexpected Error Occurs   {e}"
            ) from e
    
    
    def loggedIn(self,*,username:str,password:str,session:Session):
        
        #  first check Username exist with this username 
        try:
            if not  self.usernameExist(username=username,session=session):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Username not found"
                )
                
            # if not verify_password()    
            
            
                 
            ...
        
        except HTTPException as e:
            ...
        
        
        
        except Exception as e:
            ...        
            
        
        ...
        
        
        
        
    
            
            
instituteCore=InstituteCrud()            
              
        
        