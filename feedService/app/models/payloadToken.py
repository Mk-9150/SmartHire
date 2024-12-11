from sqlmodel  import SQLModel 
class TokenPayload(SQLModel):
    id:int
    username:str