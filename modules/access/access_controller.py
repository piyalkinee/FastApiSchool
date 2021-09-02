from modules.access.access_scheme import Token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database.coredb import get_db
from sqlalchemy.orm import Session
from .services.autorization import authenticate_user
from .services.passtools import generate, get_password_hash
from .services.jwttool import get_access_token
from ..user.user_models import UserDB
from ..user.user_schemas import UserCreate
from .access_scheme import Token

routes = APIRouter(prefix="/access", tags=["Access"])


@routes.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.disabled or user.deleted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = get_access_token(user.name)

    return {"access_token": token, "token_type": "bearer"}


@routes.post("/registration")
async def registration(user_data: UserCreate, db: Session = Depends(get_db)):

    user_with_name = db.query(UserDB).filter(
        UserDB.name == user_data.name).first()
    if user_with_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This name is already in use"
        )

    user_with_email = db.query(UserDB).filter(
        UserDB.email == user_data.email).first()

    if user_with_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already in use"
        )

    user_data_without_password = user_data.dict()

    del user_data_without_password["password"]

    new_user = UserDB(**user_data_without_password)

    salt = generate(6)

    new_user.password_salt = salt
    new_user.password_hash = get_password_hash(user_data.password, salt)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return "User registrated sucsess"
