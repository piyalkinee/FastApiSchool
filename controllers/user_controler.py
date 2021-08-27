from fastapi import APIRouter, Depends, HTTPException, status
from database.coredb import get_db
from services.autorization import oauth2_scheme, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

routes = APIRouter(prefix="/user", tags=["User"])


@routes.get("/getOne")
async def studentsGetOne(token: str = Depends(oauth2_scheme)):
    return {"students"}


@routes.post("/create")
async def studentsCreate():
    return {"students"}


@routes.put("/update")
async def studentsUpdate():
    return {"students"}


@routes.delete("/delete")
async def studentsDelete():
    return {"students"}
