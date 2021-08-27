from fastapi import APIRouter, Depends, HTTPException, status
from services.Autorization import oauth2_scheme, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm

routes = APIRouter(prefix="/students", tags=["Students"])

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"access_token": user.name, "token_type": "bearer"}

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
