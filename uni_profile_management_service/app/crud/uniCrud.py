from sqlmodel import select , Session , Sequence 
from fastapi  import HTTPException , status
from sqlalchemy  import Engine
from sqlalchemy.orm import selectinload , joinedload , Load
from sqlalchemy.orm.attributes import flag_modified
from app.models import model


class UniVersityCrud():
    
    def CreateUni(self,*,uni_create:model.Unicreate,session:Session ):
        ...
        try:
            ...
            # return uni_create
            uni = model.University.model_validate(uni_create)
            # return uni
            session.add(uni)
            session.commit()
            session.refresh(uni)
            return uni
        

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   from e 
    
    
    def updateUni(self, *,  uni_id:int, uni_update:model.UpdateModel, session:Session):
        try:
            uni = session.get(model.University, uni_id)
            if not uni:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="University not found")
            
            
            uni_data = uni_update.model_dump(exclude_unset=True)
            
            uni.sqlmodel_update(uni_data)
            # for key, value in uni_data.items():
            #     setattr(uni, key, value)
            session.add(uni)
            session.commit()
            session.refresh(uni)
            return uni
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   from e


uniprofilecrud=UniVersityCrud()           
