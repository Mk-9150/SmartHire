from sqlmodel import SQLModel , Field
from datetime import datetime , timezone



class BaseIdModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Timezone-aware UTC datetime
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}  # Automatically updated in UTC
    )