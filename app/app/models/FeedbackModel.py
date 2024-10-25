class Feedback(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str
    feedback_date: str
    teacher_id: Optional[int] = Field(foreign_key="teacher.id")
    institute_id: Optional[int] = Field(foreign_key="institute.id")
