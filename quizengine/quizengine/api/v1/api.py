from fastapi import APIRouter
from quizengine.api.v1.Routes import quiz
from quizengine.api.v1.Routes import topic
from quizengine.api.v1.Routes import quizquestion
from quizengine.api.v1.Routes import health
from quizengine.api.v1.Routes import question
from quizengine.api.v1.Routes import quizSetting


apiRoute=APIRouter()

apiRoute.include_router(quiz.router , prefix="/quiz",tags=["Quiz"])
apiRoute.include_router(topic.router,prefix="/topic",tags=["Topics"]) 
apiRoute.include_router(quizquestion.router,prefix="/quizques",tags=["Link QuizQues"]) 
apiRoute.include_router(quizSetting.router,prefix="/setting",tags=["Quiz Settings"]) 
apiRoute.include_router(question.router,prefix="/question",tags=["Questions"]) 
apiRoute.include_router(health.router,prefix="/health",tags=["Check Health"]) 