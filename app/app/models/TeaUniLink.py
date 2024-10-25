from sqlmodel import Field , SQLModel


class TeacherUniLink(SQLModel,table=True):
    """
         ...
    """
    teacher_id:int|None=Field(default=None, foreign_key="teacher.id" , primary_key=True)
    institute_id:int|None=Field(default=None,foreign_key="institute.id" , primary_key=True)
    
    
    