from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from models.user_models import UserDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Проверка введеного пароля и хешированного из бд
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Хеширование пароля
def get_password_hash(password):
    return pwd_context.hash(password)


# Получить модель пользователя с именем
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


# Вернуть модель пользователя если все проверки пройдены
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
