from database.coredb import Base
from sqlalchemy import Column,Table,ForeignKey

user_course = Table('user_course', Base.metadata,
    Column('user', ForeignKey('users.id'), primary_key=True),
    Column('course', ForeignKey('courses.id'), primary_key=True)
)