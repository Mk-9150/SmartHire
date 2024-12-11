from fastapi import HTTPException , status
from sqlmodel import Session  , select
from app.models import certifications_model
from sqlalchemy.orm import selectinload , joinedload , Load 
from app.models import teacher_model
import uuid
import os
from typing import Any

class CertificationCrud():
    async def POst_certification(self,teacher_id:int,text:str ,image_file:Any,session:Session):
        try:
            # teacher=session.get(teacher_model.Teacher,teacher_id)
            image_type:list[str]=["jpg","png","jpeg"]
            fileExt= image_file.content_type.split("/")[1]
            if fileExt  not in image_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid image type"
                )
            
            file_name=f"{uuid.uuid4()}.{image_file.content_type.split("/")[-1]}"
            
            teacher:teacher_model.Teacher=session.exec(
                select(teacher_model.Teacher)
                .options(selectinload(teacher_model.Teacher.certifications), Load(teacher_model.Teacher).raiseload("*"))
                .where(teacher_model.Teacher.id == teacher_id)
                ).one_or_none()
            
            if not teacher:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Teacher with id {teacher_id} not found"
                )
            
            if fileExt not  in image_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid image type"
                )
                
            pathIs="app/usersCertifications/certifi/"
            newDirectory=teacher.username
            # newDirectory="zaen"
            pathIs=os.path.join(pathIs, newDirectory)
            
            try:
                ...
                # return pathIs
                os.mkdir(pathIs)
                print("Directory Created")
                myPathIs=os.path.join(pathIs, file_name)
                try:
                    with open(myPathIs, "wb") as f:
                        f.write(await image_file.read())

                    certification:certifications_model.Certification=certifications_model.Certification(text=text, certi_path_images=myPathIs, certi_type=fileExt)
                    # return certification
                    teacher.certifications.append(certification)
                    session.add(teacher)
                    session.commit()
                    return teacher.certifications
                except FileExistsError as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"{e} , picture not uploaded   due to connection , the internet is unstable"
                    ) from e
                
            except FileExistsError as e :
                
                print("Directory already exist")
                myPathIs=os.path.join(pathIs, file_name)
                try:
                    with open(myPathIs, "wb") as f:
                        f.write(await image_file.read())
                    
                    certification:certifications_model.Certification=certifications_model.Certification(text=text ,certi_path_images=myPathIs,certi_type=fileExt)        
                    # return certification
                    teacher.certifications.append(certification)
                    session.add(teacher)
                    session.commit()
                    return teacher.certifications
                
                except FileExistsError as e:
                     raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"{e} , picture not uploaded   due to connection , the internet is unstable"
                    ) from e
            
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}") from e    
                
        except  Exception as e:
            raise HTTPException (
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{e}"
            )  from e
            
                
    def deleteCertifications(self, certification_id:int , session:Session):
        try:
            certification=session.get(certifications_model.Certification, certification_id)
            if not certification:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Certification with id {certification_id} not found"
                )
            session.delete(certification)
            session.commit()
            return {"message": "Certification deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}") from e
            
certifi=CertificationCrud()



            
