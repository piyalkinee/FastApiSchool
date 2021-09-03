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


class User(BaseModel):
    name: str
    email: Optional[str] = None
    group: str
    time_of_creation: datetime
    admin: bool
    disabled: bool

    class Config:
        orm_mode = True
