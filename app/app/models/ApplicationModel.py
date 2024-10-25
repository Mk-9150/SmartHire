class Application(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    job_opening_id: int = Field(foreign_key="jobopening.id")
    teacher_id: int = Field(foreign_key="teacher.id")
    application_date: str
    status: str