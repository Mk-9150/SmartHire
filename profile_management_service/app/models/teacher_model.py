from datetime import date
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from app.models.skill_teacher_link_model import TeacherSkill
from typing import TYPE_CHECKING
from app.models.baseModels import BaseIdModel

if TYPE_CHECKING :
    ...
    from app.models.skills_models import Skill
    from app.models.education_model import Education
    from app.models.certifications_model import Certification
    

class Base(SQLModel):
    ...
    username:Optional[str]= Field(default_factory=lambda : "" ,index=True ,unique=True )
    email: str = Field(index=True, unique=True) 
    bio: Optional[str] = Field(default=None)
    years_of_experience: Optional[int] = Field(default=0)
    subjects_of_interest: Optional[str] = Field(default=None)  # e.g., "Math, Science"
    location: Optional[str] = Field(default=None)
    date_of_birth: Optional[date] = Field(default=None)
    

class TeachrCreate(Base):
    ...

class UpdateModel(SQLModel):
    ...
    # username:str= Field(index=True ,unique=True )
    # email: str = Field(index=True, unique=True) 
    bio: Optional[str] = Field(default=None)
    years_of_experience: Optional[int] = Field(default=0)
    subjects_of_interest: Optional[str] = Field(default=None)  # e.g., "Math, Science"
    location: Optional[str] = Field(default=None)
    date_of_birth: Optional[date] = Field(default=None)
    


class Teacher(BaseIdModel,Base ,table=True):
    # id: Optional[int] = Field(default=None, primary_key=True)
    # username:str= Field(index=True ,unique=True )
    # email: str = Field(index=True, unique=True)
    # password: str
    # bio: Optional[str] = Field(default=None)
    # years_of_experience: Optional[int] = Field(default=0)
    # subjects_of_interest: Optional[str] = Field(default=None)  # e.g., "Math, Science"
    # location: Optional[str] = Field(default=None)
    # date_of_birth: Optional[date] = Field(default=None)
    followers_count: Optional[int] = Field(default=0)
    institutes_followed_count: Optional[int] = Field(default=0)
    applied_tests_count: Optional[int] = Field(default=0)
    profile_picture_url: Optional[str] = Field(default=None)
    
    # created_at: date = Field(default_factory=date.today)

    # Relationships
    educations: "Education" = Relationship(
        back_populates="teacher" ,
        sa_relationship_kwargs={ 
            "lazy":"selectin",
            "cascade":"all,delete,delete-orphan"
            })
    certifications: List["Certification"] = Relationship(
        back_populates="teacher" ,
        sa_relationship_kwargs={
            "lazy":"selectin",
            "cascade":"all,delete,delete-orphan"
            }
        )
    # languages: List["Language"] = Relationship(back_populates="teacher")
    skills: List["Skill"] = Relationship(
        back_populates="teachers",
        link_model=TeacherSkill ,
        sa_relationship_kwargs={
        "lazy":"selectin", 
        # "cascade":"all,delete,delete-orphan"
            }
                )
    
    
