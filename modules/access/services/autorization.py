from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm.session import Session
from database.coredb import get_db
from modules.user.user_models import UserDB
from modules.user.user_schemas import UserResponse
from .passtools import verify_password
from .jwttool import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/access/token")


# Получить модель пользователя с именем
def get_user(db: Session, username: str):
    user = db.query(UserDB).filter(UserDB.name == username).first()
    if user != None:
        return user
    return None


# Вернуть модель пользователя если все проверки пройдены
async def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not await verify_password(password, user.password_hash, user.password_salt):
        return False
    return user


# Получение текущего пользователя
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token, credentials_exception)
    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Проверка на доступ к системе
def get_current_active_user(current_user: UserResponse = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
