from modules.access.access_scheme import Token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database.coredb import get_db
from sqlalchemy.orm import Session
from .services.autorization import authenticate_user
from .services.jwttool import get_access_token
from ..user.user_models import create, check_name, check_email
from ..user.user_schemas import UserCreate
from .access_scheme import Token

routes = APIRouter(prefix="/access", tags=["Access"])


@routes.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
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
async def registration(user_data: UserCreate):

    if check_name(user_data.name) == True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This name is already in use"
        )

    if check_email(user_data.email) == True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already in use"
        )

    await create(user_data)

    return "User registrated sucsess"
