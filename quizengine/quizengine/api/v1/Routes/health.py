from quizengine.models.health_models import (
    Health,Status,Stats
)

from quizengine.core.loggerconfig import loggerconfigu
# from sqlmodel import Session,text
# from quizengine.settings import ENV
from fastapi import APIRouter
from quizengine.api.deps import DbDependency
from quizengine.crud.healthCrud import get_Health , getStats


logger=loggerconfigu(__name__)

router= APIRouter()

@router.get("/")
def DbHealth(db:DbDependency):
    
    return get_Health(db)


@router.get("/stats")
def DbHealth(db:DbDependency):
    
    return getStats(db)

    

