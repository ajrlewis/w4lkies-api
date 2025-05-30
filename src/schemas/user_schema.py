from typing import List, Optional, Union
from datetime import datetime

from pydantic import BaseModel


class UserSnippetSchema(BaseModel):
    user_id: int
    username: str


class UserBaseSchema(BaseModel):
    username: str
    email: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
    phone: Union[str, None] = None


class UserSchema(UserBaseSchema):
    user_id: int
    is_admin: int
    is_active: int

    class Config:
        from_attributes = True
