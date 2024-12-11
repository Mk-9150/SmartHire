from sqlmodel import SQLModel
from pydantic import model_validator
class PayloadToken(SQLModel):
    ...
    id:int
    username:str
    