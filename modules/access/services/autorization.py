from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm.session import Session
from database.coredb import get_db, database
from modules.user.user_models import UserDBAsync, UserDB
from modules.user.user_schemas import User
from .passtools import verify_password
from .jwttool import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/access/token")


# Получить модель пользователя с именем
async def get_user(username: str):
    user = dict(await database.fetch_one(UserDBAsync.select().where(UserDBAsync.c.name == username)))
    if user != None:
        return user
    return None


# Вернуть модель пользователя если все проверки пройдены
async def authenticate_user(username: str, password: str):
    user = UserDB(** await get_user(username))
    if not user:
        return False
    if not await verify_password(password, user.password_hash, user.password_salt):
        return False
    return user


# Получение текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token, credentials_exception)
    user = UserDB(**await get_user(token_data.username))
    if user is None:
        raise credentials_exception
    return user


# Проверка на доступ к системе
def get_current_active_user(current_user: UserDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
