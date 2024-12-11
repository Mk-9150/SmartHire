from sqlmodel import SQLModel
from pydantic  import model_validator
class TokenPayload(SQLModel):
    id:int
    username:str
    
    
    
    @model_validator(mode="after")
    def  chkTypes(self):
        if isinstance(self.id, str):
            self.id = int(self.id)
            return self
        
        
        