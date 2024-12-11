from sqlmodel import SQLModel, Session , create_engine 
from  app.core.settings import setting


engine = create_engine(setting.DATABASE_URL , echo=True , pool_recycle=300)

        