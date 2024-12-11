from fastapi import HTTPException , status 
from sqlmodel import Session , select
from sqlalchemy.orm import  selectinload , joinedload , Load
from app.models import education_model
from app.models import teacher_model


class EducationCrud():
    
    def post_education(self,teacher_id:int,c_education:education_model.CreateEducation,session:Session):
        try:
            ...
            
            # teacher:teacher_model.Teacher=session.exec(select(teacher_model.Teacher).where(teacher_model.Teacher.id == teacher_id)).one_or_none()
            teacher:teacher_model.Teacher=session.exec(
                select(teacher_model.Teacher)
                .options(selectinload(teacher_model.Teacher.educations) , Load(teacher_model.Teacher).raiseload("*"))
                .execution_options(populate_existing=True)
                .where(teacher_model.Teacher.id == teacher_id)
                ).one_or_none()
            
            education:education_model.Education=education_model.Education.model_validate(c_education)
            
            teacher.educations = education
            session.add(teacher)
            session.commit()
            session.refresh(teacher)
            return teacher
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Something went wrong") 
            
            
            
edu=EducationCrud()            