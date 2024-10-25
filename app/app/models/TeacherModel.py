from sqlmodel import Field,Relationship
from app.models.BaseModel import BaseModelID
from typing import TYPE_CHECKING,Annotated
from app.models.TeaUniLink import TeacherUniLink
from sqlmodel import SQLModel
if TYPE_CHECKING :
    from app.models.Institute_model import Institute


class BaseT(SQLModel):
    
    name: Annotated[str,Field()]
    email: str=Field()
    profile_description: str
    address: str

    ...
    

class TeacherCreate(BaseT):
    
    password:str=Field(min_length=10)
    acedimics:str
    
    
    ...    

class Teacher(BaseModelID,BaseT,table=True):

    hash_Password:str=Field(min_length=10)
    acedimics:str
    institutes:list["Institute"]=Relationship(back_populates="teachers",link_model=TeacherUniLink)
    
    # test_score: Optional[float] = None
    # applications: List["Application"] = Relationship(back_populates="teacher")
    # likeorCommentId:Annotated[Optional[int],Field(default=None,foreign_key="likeandcomment.id")]
    # haveLikeComment:List["LikeandComment"]=Relationship(back_populates="likeorCommentTo")
    # interviews: List["Interview"] = Relationship(back_populates="teacher")

