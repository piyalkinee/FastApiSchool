from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from database.coredb import Base
from database.association_models import user_course


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(256), unique=True)
    email = Column(String(256), unique=True)
    password_hash = Column(String(256))
    password_salt = Column(String(256))
    group = Column(String(256), default="student")
    time_of_creation = Column(DateTime, default=datetime.now())
    admin = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    participation_in_courses = relationship(
        "CourseDB",
        secondary=user_course,
        back_populates="users_in_course")
