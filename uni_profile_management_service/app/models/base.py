from sqlmodel import SQLModel , Field
from typing  import Optional
import datetime
import pytz
class BaseDateTime():
    id:Optional[int] = Field(default=None,primary_key=True)
    created_at:datetime.datetime = Field(default_factory= lambda :datetime.datetime.now(datetime.timezone.utc))
    updated_at:datetime.datetime = Field(
           default_factory= lambda :datetime.datetime.now(datetime.timezone.utc),
           sa_column_kwargs={"onupdate": lambda :datetime.datetime.now(datetime.timezone.utc)}
        )
    
   
     