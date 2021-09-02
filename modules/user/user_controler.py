from fastapi import APIRouter, Depends, HTTPException, status
from database.coredb import get_db
from sqlalchemy.orm import Session
from .user_models import UserDB
from .user_schemas import UserUpdate, UserResponse
from modules.access.services.autorization import get_current_active_user, verify_password
from modules.access.services.passtools import get_password_hash

routes = APIRouter(prefix="/user", tags=["User"])


@routes.get("/getOne/{user_id}", response_model=UserResponse)
async def user_get_one(user_id: int, auth_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    user_from_db = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    return user_from_db.__dict__


@routes.put("/update/{user_id}")
async def user_update(user_id: int, user_update_data: UserUpdate, auth_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    user_for_update = db.query(UserDB).filter(UserDB.id == user_id).first()

    if user_update_data.name != None:

        user_with_name = db.query(UserDB).filter(
            UserDB.name == user_update_data.name).first()

        if not user_with_name:
            user_for_update.name = user_update_data.name
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This name is already in use"
            )

    if user_update_data.email != None:

        user_with_email = db.query(UserDB).filter(
            UserDB.email == user_update_data.email).first()

        if not user_with_email:
            user_for_update.email = user_update_data.email
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already in use"
            )

    if user_update_data.password_new != None:

        if not user_update_data.password_old:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password not specified"
            )
        if not verify_password(user_update_data.password_old, user_for_update.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password specified incorrectly"
            )
        user_for_update.password = get_password_hash(
            user_update_data.password_new)

    db.commit()
    db.refresh(user_for_update)

    return f"User with id:{user_id} updated"


@routes.delete("/delete/{user_id}")
async def user_delete(user_id: int, auth_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    user_for_delete = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user_for_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    user_for_delete.deleted = True
    db.commit()
    db.refresh(user_for_delete)

    return f"User with id:{user_id} deleted"
