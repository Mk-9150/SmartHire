from sqlmodel import create_engine , Session , SQLModel
from quizengine import settings
connection_Str=str(settings.DATABASE_URL)


# print(connection_Str)

engine = create_engine(connection_Str , echo=True , pool_recycle=300)

