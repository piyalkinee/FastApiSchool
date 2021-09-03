from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from database.coredb import Base, database
from database.association_models import user_course
from .user_schemas import UserCreate, UserUpdate
from modules.access.services.passtools import generate, verify_password, get_password_hash


# UserDBAsync = Table(
#    "users",
#    metadata,
#    Column("id", Integer, primary_key=True, index=True, unique=True),
#    Column("name", String(256), unique=True, index=True),
#    Column("email", String(256), unique=True, index=True),
#    Column("password_hash", String(256)),
#    Column("password_salt", String(256)),
#    Column("group", String(256), default="student"),
#    Column("time_of_creation", DateTime, default=datetime.now()),
#    Column("admin", Boolean, default=False),
#    Column("disabled", Boolean, default=False),
#    Column("deleted", Boolean, default=False)
# )


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


UserDBAsync = UserDB.__table__

# Work with model


async def get_one(id: int):
    user = dict(await database.fetch_one(UserDBAsync.select().where(UserDBAsync.c.id == id)))
    return user


async def create(user_data: UserCreate):
    user_data_to_db = user_data.dict()

    del user_data_to_db["password"]

    salt = generate(6)
    
    user_data_to_db["password_salt"] = salt
    user_data_to_db["password_hash"] = await get_password_hash(user_data.password, salt)
    user_data_to_db["group"] = "student"
    user_data_to_db["time_of_creation"] = datetime.now()
    user_data_to_db["admin"] = False
    user_data_to_db["disabled"] = False
    user_data_to_db["deleted"] = False

    query = UserDBAsync.insert().values(**user_data_to_db)

    await database.execute(query)


async def update(id: int, user_update_data: UserUpdate, password_hash: str = None):
    user_for_update = dict(await database.fetch_one(UserDBAsync.select().where(UserDBAsync.c.id == id)))
    del user_for_update["id"]

    if user_update_data.name != None:
        user_for_update["name"] = user_update_data.name

    if user_update_data.email != None:
        user_for_update["email"] = user_update_data.email

    if password_hash != None:
        user_for_update["password_hash"] = password_hash

    query = UserDBAsync.update().where(
        UserDBAsync.c.id == id).values(**user_for_update)
    await database.execute(query)


async def delete(id: int):
    user_for_delete = dict(await database.fetch_one(UserDBAsync.select().where(UserDBAsync.c.id == id)))
    del user_for_delete["id"]
    user_for_delete["deleted"] = True
    query = UserDBAsync.update().where(
        UserDBAsync.c.id == id).values(**user_for_delete)
    await database.execute(query)


# Check data


async def check_id(id: int):
    check = await database.fetch_one(UserDBAsync.select().where(UserDBAsync.c.id == id))
    if check != None:
        return True
    return False


async def check_name(name: str):
    check = await database.fetch_one(UserDBAsync.select().where(UserDBAsync.c.name == name))
    if check != None:
        return True
    return False


async def check_email(email: str):
    check = await database.fetch_one(UserDBAsync.select().where(UserDBAsync.c.email == email))
    if check != None:
        return True
    return False


async def check_newpassword(id: int, password_old: str):
    check = UserDB(** dict(await database.fetch_one(UserDBAsync.select().where(UserDBAsync.c.id == id))))
    if not verify_password(password_old, check.password_hash, check.password_salt):
        return None
    return check.password_salt
