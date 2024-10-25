from sqlmodel import create_engine

from app.core.app_settings import setting


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL

connection_string = setting.DATABASE_URL.replace(
    "postgresql", "postgresql+psycopg"
)

# print(connection_string2)

engine=create_engine(connection_string,connect_args={},pool_recycle=300)
print(engine)


