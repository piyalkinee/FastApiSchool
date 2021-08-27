from datetime import datetime
from database.coredb import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, index=True, unique=True)
