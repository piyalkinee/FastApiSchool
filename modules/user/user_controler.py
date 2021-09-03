from modules.course.course_models import check_id
from fastapi import APIRouter, Depends, HTTPException, status
from .user_models import UserDB, get_one, update, delete, check_name, check_email, check_newpassword
from .user_schemas import UserUpdate, User
from modules.access.services.autorization import get_current_active_user
from modules.access.services.passtools import get_password_hash

routes = APIRouter(prefix="/user", tags=["User"])


@routes.get("/getOne/{user_id}", response_model=User)
async def user_get_one(user_id: int, auth_user: UserDB = Depends(get_current_active_user)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    user = await get_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    return user


@routes.put("/update/{user_id}")
async def user_update(user_id: int, user_update_data: UserUpdate, auth_user: UserDB = Depends(get_current_active_user)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    user_for_update = UserDB(** await get_one(user_id))
    if user_for_update == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    if user_update_data.name != None:
        if await check_name(user_update_data.name) == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This name is already in use"
            )

    if user_update_data.email != None:
        if await check_email(user_update_data.email) == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already in use"
            )

    new_password_hash = None

    if user_update_data.password_new != None:
        salt = await check_newpassword(user_id, user_update_data.password_old)
        if salt == None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password specified incorrectly"
            )
        new_password_hash = await get_password_hash(
            user_update_data.password_new, salt)

    await update(user_id, user_update_data, new_password_hash)

    return f"User with id:{user_id} updated"


@routes.delete("/delete/{user_id}")
async def user_delete(user_id: int, auth_user: UserDB = Depends(get_current_active_user)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    if check_id(user_id) == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    await delete(user_id)

    return f"User with id:{user_id} deleted"
