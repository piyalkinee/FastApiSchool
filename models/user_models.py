from typing import Optional
from pydantic import BaseModel
from database.coredb import Base
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    disabled: Optional[bool] = False


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(256))
    email = Column(String(256), unique=True)
    password = Column(String(256))
    group = Column(String(256), default="student")
    time_of_creation = Column(DateTime, default=datetime.now())
    admin = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
