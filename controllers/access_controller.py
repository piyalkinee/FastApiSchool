from fastapi import APIRouter, Depends, HTTPException, status
from database.coredb import get_db
from services.autorization import authenticate_user, get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.user_models import UserCreate, UserDB

routes = APIRouter(prefix="/access", tags=["Access"])


@routes.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"access_token": user.name, "token_type": "bearer"}


@routes.post("/registration")
async def registration(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = UserDB(**user_data.dict())
    new_user.password = get_password_hash(user_data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "User registrated sucsess"
