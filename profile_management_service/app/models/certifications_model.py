from typing import Optional , TYPE_CHECKING , Annotated
from sqlmodel import SQLModel, Field, Relationship
from datetime import date



if TYPE_CHECKING:
    from app.models.teacher_model import Teacher
    

class Base(SQLModel):
    text: str  # e.g., "About certifications"
    certi_path_images:str
    certi_type:Annotated[str,Field()]    #e.g [png , jpeg]  
    # issuer: Optional[str] = Field(default=None)  # e.g., "International TESOL Organization"
    # date_awarded: Optional[date] = Field(default=None)
        
class CertificationText(SQLModel):
    text:Annotated[str,Field(default=None)]    
        
class CreateCertification(Base):
    ...

class ReadCertification(Base):
    id: int

class Certification(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teacher_id: int = Field(foreign_key="teacher.id")
    
    # Relationship back to Teacher
    teacher: "Teacher" = Relationship(back_populates="certifications")