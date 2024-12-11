from sqlmodel  import SQLModel , Field , Column , Relationship
from typing import Annotated , List , Union , Optional
from sqlalchemy.dialects.postgresql  import JSON
from datetime import datetime  , timezone
from pydantic import model_validator
import pytz
from typing_extensions import Self

class BasePost(SQLModel):
    ...
    title: str
    description: str
    location: Optional[str] = None
    skills_required: Optional[list[str]] = Field(sa_column=Column(JSON) , default_factory=list)    # Use JSON serialization for lists
    experience_needed: Optional[str] = None
    employment_type: Optional[str] = None  # E.g., "Full-time", "Part-time"
    salary_range: Optional[str] = None

    application_deadline: datetime = Field()  # Deadline for applications
    quiz_date: datetime = Field()  # Schedule for the quiz
    quiz_duration: Optional[int] = None  # Duration of the quiz in minutes

    


class JobPosting(BasePost, table=True):
    id:Optional[int] = Field(default_factory=lambda :None, primary_key=True)
    username:Optional[str]=Field(index=True)
    university_id: int = Field(index=True) 
    posted_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    is_active: bool = Field(default=True)
    haveAppliers:Optional[list["JobApplication"]]=Relationship(
        back_populates="havepost",
        sa_relationship_kwargs={
         "cascade": "all, delete-orphan"
        }
        )
    
    
    
    @model_validator(mode="after")
    def setQuizDate_in_Utc(self)->Self:
        self.quiz_date=self.quiz_date.astimezone(pytz.utc)
        self.application_deadline=self.application_deadline.astimezone(pytz.utc)
        return self
    

class JonApplicationBase(SQLModel):
        
    text:str      #  why u interested in this job
    resume_url: Optional[str]=Field(default_factory=lambda : "")
    expereriance :str 
    # certifications :[]
    
class JobApplication(JonApplicationBase, table=True):
    id: Optional[int]= Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="jobposting.id", index=True)
    teacher_id: int = Field(index=True)  # Assuming teacher IDs are managed elsewhere
    teacher_username: str = Field(index=True)
    applied_at: datetime = Field(default_factory=lambda:datetime.now(pytz.utc)) 
    status: str = Field(default="Applied")  # E.g., "Applied", "Under Review", "Rejected"
    # resume_url: Optional[str] = None
    image_url: Optional[str] = Field(default_factory=lambda : "")
    havepost:Optional[JobPosting]=Relationship(
        back_populates="haveAppliers",
        )
        
    

    

    