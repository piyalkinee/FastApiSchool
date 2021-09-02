import random
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

genSumbols = "1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ"


# Проверка введеного пароля и хешированного из бд
async def verify_password(plain_password: str, hashed_password: str, salt: str):
    return pwd_context.verify(plain_password + salt, hashed_password)


# Хеширование пароля
async def get_password_hash(password: str, salt: str):
    return pwd_context.hash(password + salt)


# Генерация паролей
def generate(lenght: int):

    newpass = ""

    for x in range(lenght):
        newpass += random.choice(list(genSumbols))

    return newpass
