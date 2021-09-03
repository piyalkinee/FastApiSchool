from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class CourseCreate(BaseModel):
    name: str


class CourseUpdate(BaseModel):
    name: str


class CourseResponse(BaseModel):
    name: str
    user_creator_id: int
    time_of_creation: datetime
    users_in_course : List[dict]
