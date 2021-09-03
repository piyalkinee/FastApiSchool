from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request
import databases

SQLALCHEMY_DATABASE_URL = "mysql://root:1231@localhost:3306/schoolDB"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

metadata = MetaData()


async def get_db(request: Request):
    return request.state.db
