from fastapi import HTTPException , status 
from sqlmodel import SQLModel , Session , select 
from app.models import Relationship_model
from sqlalchemy.orm import selectinload  , joinedload 


class AddUsers():
    ...
    def add_user(self, * , id:int , username:str , session:Session):
        try:
            new_user=Relationship_model.User(Actualuser_id=id, username=username)
            session.add(new_user)
            session.commit()
            # session.refresh(new_user)
            return "user Added"
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}") from e 
        

GetInUser=AddUsers()        