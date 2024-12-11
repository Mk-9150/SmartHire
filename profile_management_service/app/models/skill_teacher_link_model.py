from sqlmodel import SQLModel, Field


# Association table for many-to-many relationship between Teacher and Skill
class TeacherSkill(SQLModel, table=True):
    teacher_id: int = Field(foreign_key="teacher.id", primary_key=True)
    skill_id: int = Field(foreign_key="skill.id", primary_key=True)