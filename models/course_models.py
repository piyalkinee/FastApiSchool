from typing import Optional
from pydantic import BaseModel
from database.coredb import Base
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.association_models import user_course


class CourseCreate(BaseModel):
    name: str


class CourseUpdate(BaseModel):
    name: str


class CourseResponse(BaseModel):
    name: str
    user_creator_id: int
    time_of_creation: datetime


class CourseDB(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(256))
    time_of_creation = Column(DateTime, default=datetime.now())
    user_creator = relationship("UserDB")
    user_creator_id = Column(Integer, ForeignKey("users.id"))
    deleted = Column(Boolean, default=False)

    users_in_course = relationship(
        "UserDB",
        secondary=user_course,
        back_populates="participation_in_courses")
