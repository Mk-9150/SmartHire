from sqlmodel import Session , select
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload , joinedload ,Load
from app.models import skills_models
from app.models import teacher_model

class SkillCrud():
    
    def post_Skill(self,teacher_id:int,skill:skills_models.CreateSkill,session:Session):
        try:
            ...
            # teacher:teacher_model.Teacher = session.get(teacher_model.Tskieacher, teacher_id)
            teacher:teacher_model.Teacher = session.exec(
                select(teacher_model.Teacher)
                .options(selectinload(teacher_model.Teacher.skills),Load(teacher_model.Teacher).raiseload("*"))
                .execution_options(populate_existing=True)
                .where(teacher_model.Teacher.id == teacher_id)
                ).unique().one_or_none()

            if not teacher:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Teacher with id {teacher_id} not found")
            
            only_skills_array:list[str]=skill.name
        
            # 1: select all the skill model first  
            # 2: before adding all the skills to the database chk the skills in createskill model already not present in database if any skill in the createkill model already exist then exclude it  from createskill model     and the skills that are not in db   make models  add to db     then make relationship to the models that createskill model have  and alredy present in db   
            # 3: in database same skill must not be replicate  
            db_skills:list[skills_models.Skill]= session.exec(select(skills_models.Skill)).all()
            
            
            skills_present_in_db_alsoIn_onlySkillsArray=set([db_skell.name for db_skell in db_skills]).intersection(set(only_skills_array)) 
            common_filtered_skills_models:list[skills_models.Skill]=[skill_modl for skill_modl in db_skills if skill_modl.name in skills_present_in_db_alsoIn_onlySkillsArray] 
            skills_that_not_in_db:list[str]=list(set(only_skills_array) - set([db_skill.name for db_skill in db_skills]))
            skill_MODELs:list[skills_models.Skill]=[]
            for s_skill in skills_that_not_in_db:
                skill_create_model:skills_models.CreateSkill=skills_models.CreateSkill(name=s_skill)
                skill_MODELs.append(skills_models.Skill.model_validate(skill_create_model))
            
            teacher.skills.extend(common_filtered_skills_models,skill_MODELs)
            session.add(teacher)
            session.commit()
            session.refresh(teacher)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Something went wrong" )
    
    
    
    # # def update_skills(self,teacher_id,skill_id:int,session:Session):
    # #     ...
    # #     try:
    # #         ...
    #         # teacher:teacher_model.Teacher=session.get(teacher_model.Teacher,teacher_id)
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                     detail="Something went wrong" )
        

skill=SkillCrud()    
    