from sqlmodel import select , Session , Sequence 
from fastapi  import HTTPException , status
from sqlalchemy  import Engine
from sqlalchemy.orm import selectinload , joinedload , Load
from sqlalchemy.orm.attributes import flag_modified
from app.models import model , TokenPayload
from app.crud.producer  import Prodducer
from aiokafka  import AIOKafkaProducer
from sqlalchemy.orm  import joinedload , selectinload  , Load
from app.core.app_setting import setting
 


class JobPostCrud():
   def createPost(self,*,uni_data:TokenPayload.PayloadToken,post_create:model.BasePost , session:Session):
      try:
         ...
         jobPost=model.JobPosting.model_validate(post_create)
         jobPost.university_id=uni_data.id
         jobPost.username=uni_data.username
         session.add(jobPost)
         session.commit()
         session.refresh(jobPost)
         return jobPost
         
      except HTTPException as e:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{str(e.detail)}"
         ) from e
         
      except Exception  as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"          
         ) from e
          
   def getPost(slef,*, uni_data:TokenPayload.PayloadToken, session:Session):
      try:
         #  at frontend handle the active  dues  jobs 
         statement=select(model.JobPosting).where(model.JobPosting.university_id==uni_data.id)
         result=session.exec(statement).all()
         return result
      except HTTPException as e:
          raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail=f"{str(e.detail)}"
          ) from e

      except Exception  as e:
          raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail=f"{str(e)}"
          ) from e    
   
   async def jobAppliers(self, user:TokenPayload.PayloadToken , applierData:model.JonApplicationBase , producer:AIOKafkaProducer,jobpost_id:int, session:Session):
      try:
         ...
         
         #  make sure no one can apply after deadline 
         ApplicationModel:model.JobApplication=model.JobApplication.model_validate(applierData)
         ApplicationModel.teacher_id=user.id
         ApplicationModel.teacher_username=user.username
         ApplicationModel.job_id=jobpost_id                  
         session.add(ApplicationModel)
         session.commit()
         session.refesh(ApplicationModel)
         
         
         await Prodducer.postEvent(applier_iid=ApplicationModel.id,userid=ApplicationModel.teacher_id , username=ApplicationModel.teacher_username,producer=producer,topic=setting.Topic_Applier)
         
         return ApplicationModel         
         
      # except HTTPException as e:
      #    raise HTTPException(
      #       status_code=status.HTTP_400_BAD_REQUEST,
      #       detail=f"{str(e.detail)}"
      #    ) from e

      except Exception  as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
         ) from e        
   
   
   
   def getAppliers_specific_job(self,jobpost_id:int , univeristy_id:int,session:Session):
      ...
      try:
         ...
         Jobpost:model.JobPosting=session.exec(select(model.JobPosting)
                                               .options(selectinload(model.JobPosting.haveAppliers) )
                                               .execution_options(populate_existing=True)
                                               .where(model.JobPosting.id==jobpost_id, model.JobPosting.university_id==univeristy_id)
                                               ).all()
         return Jobpost.haveAppliers                                             
                                               
                                               
         

      except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
         ) from e
   
   def getJobInfo(self, jobpost_id:int, session:Session):
       
      try:
         ...
         Jobpost:model.JobPosting=session.get(model.JobPosting, jobpost_id)
         return Jobpost
      except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
         ) from e
   # def getActiveJobs(self,uni_id:int ):
   #    ...
   #    try:
   #       ...
         
        
   #    except Exception as e:
   #       raise HTTPException(
   #          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
   #          detail=f"{str(e)}"
   #       ) from e   


uni_jobpost_crud=JobPostCrud()           
