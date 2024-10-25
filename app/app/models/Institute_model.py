from sqlmodel import SQLModel,create_engine,Session
from typing import Optional, List ,Annotated , Dict,Union 
import os 
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.BaseModel import BaseModelID
from typing import TYPE_CHECKING,Annotated
from app.models.TeaUniLink import TeacherUniLink
from app.models.TeacherModel import Teacher

# if TYPE_CHECKING :
    # from app.models.TeacherModel import Teacher
    
    
    

class BaseI(SQLModel):
    """
          Base Class For Institue  ! 
    """
    name: str
    email: str
    address: str
    phone_number: str
    description: str 
    
    
       
class InstituteCreate(BaseI):
    
    password:Annotated[str,Field(min_length=10)]
    website:Optional[str]=Field(default=None)
    institute_type: Optional[str]=None
    
    ...
    

    

class Institute(BaseModelID,BaseI, table=True):
    """
         Institute Class For DataBaseI Table and also used it for data validation later !
    """
    hashed_password:Annotated[str,Field(min_length=10)]
    website:Optional[str]=Field(default=None)
    institute_type: Optional[str]=None
    founded: Optional[int]=Field(default=None)
    accreditation: Optional[str]=None
    teachers:list["Teacher"] |None =Relationship(back_populates="institutes",link_model=TeacherUniLink)
    
    # job_openings: List["JobOpening"] = Relationship(back_populates="institute")
  
    
            


    

















































    


# class Teacher(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     institute:Annotated[Optional[int],Field(default=None,foreign_key="institute.id")]
#     name: str
#     email: str
#     profile_description: str
#     test_score: Optional[float] = None
#     applications: List["Application"] = Relationship(back_populates="teacher")
#     likeorCommentId:Annotated[Optional[int],Field(default=None,foreign_key="likeandcomment.id")]
#     haveLikeComment:List["LikeandComment"]=Relationship(back_populates="likeorCommentTo")
#     # interviews: List["Interview"] = Relationship(back_populates="teacher")



# class TeacherUniLink(SQLModel):
#     ...
    

# class LikeandComment(SQLModel):
#     """
#         *  also for university like or comments
#     """
#     id:Annotated[Optional[int],Field(default=None)]
#     like:Union[str,None]=None
#     comment:Optional[str]=None
#     likeorCommentFrom:Annotated[int,Field(foreign_key="teacher.id")]  
#     likeorCommentTo:Teacher=Relationship(back_populates="haveLikeComment")
#     # likeorCommetTo:Annotated[int,Field(foreign_key="teacher.id")]
       
# class JobOpening(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     institute_id: int = Field(foreign_key="institute.id")
#     title: str
#     description: str
#     test_link: str
#     institute: Institute = Relationship(back_populates="job_openings")
#     applications: List["Application"] = Relationship(back_populates="job_opening")

# class Test(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     teacherid:Annotated[Optional[int],Field(default=None , foreign_key="teacher.id")]
#     content: str

# class Application(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     job_opening_id: int = Field(foreign_key="jobopening.id")
#     teacher_id: int = Field(foreign_key="teacher.id")
#     application_date: str
#     status: str

# class Interview(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     application_id: int = Field(foreign_key="application.id")
#     interview_date: str
#     notes: str

# class Feedback(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     content: str
#     feedback_date: str
#     teacher_id: Optional[int] = Field(foreign_key="teacher.id")
#     institute_id: Optional[int] = Field(foreign_key="institute.id")
