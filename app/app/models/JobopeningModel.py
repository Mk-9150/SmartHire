class JobOpening(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    institute_id: int = Field(foreign_key="institute.id")
    title: str
    description: str
    test_link: str
    institute: Institute = Relationship(back_populates="job_openings")
    applications: List["Application"] = Relationship(back_populates="job_opening")