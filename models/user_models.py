from typing import Optional
from pydantic import BaseModel
from database.coredb import Base
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.association_models import user_course


class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password_new: Optional[str] = None
    password_old: Optional[str] = None


class UserResponse(BaseModel):
    name: str
    email: str
    group: str
    time_of_creation: datetime
    admin: bool
    disabled: bool


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(256), unique=True)
    email = Column(String(256), unique=True)
    password = Column(String(256))
    group = Column(String(256), default="student")
    time_of_creation = Column(DateTime, default=datetime.now())
    admin = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    participation_in_courses = relationship(
        "CourseDB",
        secondary=user_course,
        back_populates="users_in_course")
