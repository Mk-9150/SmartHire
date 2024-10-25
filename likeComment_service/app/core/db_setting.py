from sqlmodel import create_engine
from app.core.app_setting import setting

connection_str=setting.DATABASE_URL.replace(
     "postgresql", "postgresql+psycopg"
)

print(connection_str)

#  connection to the postgress database   # acts as a bridge 
engine=create_engine(connection_str,connect_args={},pool_recycle=300,echo=True)

