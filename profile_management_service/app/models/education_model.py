from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List , TYPE_CHECKING
from datetime import date



if TYPE_CHECKING:
    from app.models.teacher_model import Teacher


class Base(SQLModel):
    ...
    university: str  # e.g., "University of California"
    degree: str  # e.g., "Bachelor's in Education"
    graduation_year: int

class CreateEducation(Base):
    ...

class ReadEducation(Base):
    id: int
# Education Model
class Education(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teacher_id: int = Field(foreign_key="teacher.id")
    
    # Relationship back to Teacher
    teacher: "Teacher" = Relationship(back_populates="educations")

