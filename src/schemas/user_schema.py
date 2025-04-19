from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    password_hash: str
    is_admin: bool

    class Config:
        from_attributes = True
