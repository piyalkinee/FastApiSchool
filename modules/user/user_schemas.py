from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password_new: Optional[str] = None
    password_old: Optional[str] = None


class UserResponse(BaseModel):
    name: str
    email: str
    group: str
    time_of_creation: datetime
    admin: bool
    disabled: bool
