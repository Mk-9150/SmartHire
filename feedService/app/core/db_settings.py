from sqlmodel import create_engine
from app.core.app_setting import setting
connection_str=setting.DATABASE_URL.replace(
    "postgresql","postgresql+psycopg"
)
engine=create_engine(connection_str,connect_args={},pool_recycle=300, echo=True)