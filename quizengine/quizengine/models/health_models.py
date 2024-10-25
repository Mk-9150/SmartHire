from enum import Enum
from typing import Literal

from pydantic import BaseModel

class Status(str,Enum):
    OK="OK"
    NOT_OK="NOT_OK"
    
    
    
class Health(BaseModel):
    app_status: Status | None=None
    db_status: Status | None=None
    environment: Literal["development", "staging", "production"] | str | None
    
    
    


class Stats(BaseModel):
    topic: int | None=None
    # content: int | None=None
    questionbank: int | None=None
    mcqoption: int | None=None
       