from sqlmodel import SQLModel , Field


class test(SQLModel , table=True):
    id:int|None=Field(default=None,primary_key=True)
    text:str

    