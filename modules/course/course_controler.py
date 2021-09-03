from fastapi import APIRouter, Depends, HTTPException, status
from database.coredb import get_db
from modules.access.services.autorization import get_current_active_user
from sqlalchemy.orm import Session
from modules.user.user_models import UserDB
from .course_models import CourseDB, get_one, get_range, create, update, delete, check_id, check_name
from .course_schemas import CourseCreate, CourseResponse, CourseUpdate
from typing import List

routes = APIRouter(prefix="/course", tags=["Course"])


@routes.get("/getOne/{course_id}", response_model=CourseResponse)
async def course_get_one(course_id: int, auth_user: UserDB = Depends(get_current_active_user)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    course_from_db = await get_one(course_id)
    if not course_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    return course_from_db


@routes.get("/getRange/{limit}/{skip}", response_model=List[CourseResponse])
async def course_get_range(limit: int, skip: int, auth_user: UserDB = Depends(get_current_active_user)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    course_list_from_db = await get_range(limit, skip)
    if not course_list_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    return [CourseResponse(**course) for course in course_list_from_db]


@routes.post("/create", status_code=201)
async def course_create(course_data: CourseCreate, auth_user: UserDB = Depends(get_current_active_user)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    if await check_name(course_data.name) == True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This name is already in use"
        )

    await create(course_data, auth_user.id)

    return "Cource created"


@routes.put("/addUser/{course_id}/{user_id}")
async def course_add_user(course_id: int, user_id: int, auth_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    course_for_update = db.query(CourseDB).filter(
        CourseDB.id == course_id).first()
    if not course_for_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    user_from_db = db.query(UserDB).filter(
        CourseDB.id == user_id).first()
    if not course_for_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    course_for_update.users_in_course.append(user_from_db)

    db.commit()
    db.refresh(course_for_update)

    return f"User with id:{user_id} add to course with id:{course_id}"


@routes.put("/update/{course_id}")
async def course_update(course_id: int, course_data: CourseUpdate, auth_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    course_for_update = CourseDB(** await get_one(course_id))
    if course_for_update == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    if course_data.name != None:
        if await check_name(course_data.name) == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This name is already in use"
            )

    await update(course_id, course_data)

    return f"Course with id:{course_id} updated"


@routes.delete("/delete/{course_id}")
async def course_delete(course_id: int, auth_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):

    if auth_user.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    if check_id(course_id) == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    await delete(course_id)

    return f"Course with id:{course_id} deleted"
