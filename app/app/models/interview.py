class Interview(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id")
    interview_date: str
    notes: str