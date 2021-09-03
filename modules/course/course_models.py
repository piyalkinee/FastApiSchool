from datetime import datetime
from database.coredb import Base, database
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.association_models import user_course
from .course_schemas import CourseCreate, CourseUpdate
from modules.user.user_models import UserDBAsync


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


CourseDBAsync = CourseDB.__table__

# Work with model


async def get_one(id: int):
    course = dict(await database.fetch_one(CourseDBAsync.select().where(CourseDBAsync.c.id == id)))
    user_course_all = [dict(u_c) for u_c in await database.fetch_all(user_course.select().where(user_course.c.course == id))]
    course["users_in_course"] = user_course_all
    return course


async def get_range(limit: int, skip: int):
    courses = [dict(course) for course in await database.fetch_all(CourseDBAsync.select().limit(limit).offset(skip))]
    for course in courses:
        print(course)
        course["users_in_course"] = [dict(u_c) for u_c in await database.fetch_all(user_course.select().where(user_course.c.course == course["id"]))]
    return courses


async def create(course_data: CourseCreate, user_creator_id: int):
    course_data_to_db = course_data.dict()

    course_data_to_db["time_of_creation"] = datetime.now()
    course_data_to_db["user_creator_id"] = user_creator_id
    course_data_to_db["deleted"] = False

    query = CourseDBAsync.insert().values(**course_data_to_db)

    await database.execute(query)


async def update(id: int, course_update_data: CourseUpdate):
    user_for_update = dict(await database.fetch_one(CourseDBAsync.select().where(CourseDBAsync.c.id == id)))
    del user_for_update["id"]

    if course_update_data.name != None:
        user_for_update["name"] = course_update_data.name

    query = CourseDBAsync.update().where(
        CourseDBAsync.c.id == id).values(**user_for_update)
    await database.execute(query)


async def add_user_to_course(course_id: int, user_id: int):
    query = user_course.insert().values(user=user_id, course=course_id)

    await database.execute(query)


async def delete(id: int):
    course_for_delete = dict(await database.fetch_one(CourseDBAsync.select().where(CourseDBAsync.c.id == id)))
    del course_for_delete["id"]
    course_for_delete["deleted"] = True
    query = CourseDBAsync.update().where(
        CourseDBAsync.c.id == id).values(**course_for_delete)
    await database.execute(query)

# Check data


async def check_id(id: int):
    check = await database.fetch_one(CourseDBAsync.select().where(CourseDBAsync.c.id == id))
    if check != None:
        return True
    return False


async def check_name(name: str):
    check = await database.fetch_one(CourseDBAsync.select().where(CourseDBAsync.c.name == name))
    if check != None:
        return True
    return False
