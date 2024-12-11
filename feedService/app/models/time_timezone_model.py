import datetime
from sqlmodel import SQLModel,Field
from typing import Annotated
from pydantic  import model_validator
import pytz


class LocalTimePlus_imeTimeZone(SQLModel):
    timezone:Annotated[str,Field()]
    localTime:Annotated[datetime.datetime,Field()]
    


class LocalTimePlus_imeTimeZone_create(LocalTimePlus_imeTimeZone):
    ...
    
    
    #  
    @model_validator(mode="after")
    def make_Time_Zone_Aware(self):
        if isinstance(self.localTime, datetime.datetime):
            self.localTime = self.localTime.astimezone(pytz.timezone(self.timezone))
            return self
    
    
    @model_validator(mode="after")
    def  convertDateTimeTo_IsoFormet(self):
        if isinstance(self.localTime , datetime.datetime):
            self.localTime = self.localTime.isoformat()
            return self  
    # class Config:
    #     json_encoders = {
    #         datetime.datetime: lambda v: v.isoformat()  # Automatically serialize datetime to ISO-8601
    #     }