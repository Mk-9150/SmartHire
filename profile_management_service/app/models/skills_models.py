from sqlmodel import SQLModel , Field, Relationship
from typing import Optional, List
from typing import TYPE_CHECKING
from app.models.skill_teacher_link_model import TeacherSkill
from typing import Annotated
if TYPE_CHECKING :
    from app.models.teacher_model import Teacher


class Base(SQLModel):
    name:Annotated[list[str],Field(default=None)]

class CreateSkill(Base):
    ...

class ReadSkill(Base):
    id: int

# class updateSkill(SQLModel):
    # name:Annotated[list[str],Field(default=None)]

class Skill(SQLModel , table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Python", "Project Management"
    
    # Relationship to Teacher through TeacherSkill
    teachers: List["Teacher"] = Relationship(back_populates="skills", link_model=TeacherSkill)