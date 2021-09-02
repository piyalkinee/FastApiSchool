from fastapi import APIRouter, Depends, HTTPException, status
from database.coredb import get_db
from modules.access.services.autorization import oauth2_scheme
from sqlalchemy.orm import Session
from modules.user.user_models import UserDB
from .course_models import CourseDB
from .course_schemas import CourseCreate, CourseResponse, CourseUpdate
from typing import List

routes = APIRouter(prefix="/course", tags=["Course"])


@routes.get("/getOne/{course_id}", response_model=CourseResponse)
async def course_get_one(course_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user_executor = db.query(UserDB).filter(UserDB.name == token).first()
    if not user_executor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access is denied"
        )

    if user_executor.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    course_from_db = db.query(CourseDB).filter(
        CourseDB.id == course_id).first()

    if not course_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    return course_from_db.__dict__


@routes.get("/getRange/{limit}/{skip}", response_model=List[CourseResponse])
async def course_get_one(limit: int, skip: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user_executor = db.query(UserDB).filter(UserDB.name == token).first()
    if not user_executor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access is denied"
        )

    if user_executor.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    course_list_from_db = db.query(CourseDB).limit(limit).offset(skip).all()

    if not course_list_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    return [CourseResponse(**result.__dict__) for result in course_list_from_db]


@routes.post("/create")
async def course_create(course_data: CourseCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user_executor = db.query(UserDB).filter(UserDB.name == token).first()
    if not user_executor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access is denied"
        )

    if user_executor.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    user_with_name = db.query(CourseDB).filter(
        CourseDB.name == course_data.name).first()
    if user_with_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This name is already in use"
        )

    new_course = CourseDB(**course_data.dict())
    new_course.user_creator_id = user_executor.id
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return "Cource created"


@routes.put("/addUser/{course_id}/{user_id}")
async def course_add_user(course_id: int, user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_executor = db.query(UserDB).filter(UserDB.name == token).first()
    if not user_executor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access is denied"
        )

    if user_executor.admin != True:
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
async def course_update(course_id: int, course_data: CourseUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user_executor = db.query(UserDB).filter(UserDB.name == token).first()
    if not user_executor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access is denied"
        )

    if user_executor.admin != True:
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

    if course_data.name != None:

        course_with_name = db.query(CourseDB).filter(
            CourseDB.name == course_data.name).first()

        if not course_with_name:
            course_for_update.name = course_data.name
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This name is already in use"
            )

    db.commit()
    db.refresh(course_for_update)

    return f"Course with id:{course_id} updated"


@routes.delete("/delete/{course_id}")
async def course_delete(course_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user_executor = db.query(UserDB).filter(UserDB.name == token).first()
    if not user_executor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access is denied"
        )

    if user_executor.admin != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is denied"
        )

    course_for_delete = db.query(CourseDB).filter(
        CourseDB.id == course_id).first()
    if not course_for_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    course_for_delete.deleted = True
    db.commit()
    db.refresh(course_for_delete)

    return f"Course with id:{course_id} deleted"
