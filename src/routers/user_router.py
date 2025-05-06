from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger

from cruds import user_crud
from dependencies import GetDBDep, GetCurrentUserDep, GetCurrentAdminUserDep
from exceptions import DatabaseError
from schemas.user_schema import UserSchema


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/", response_model=list[UserSchema])
async def read_users(
    db: GetDBDep, current_user: GetCurrentAdminUserDep
) -> list[UserSchema]:
    """Reads and returns all users from the database."""
    try:
        users = user_crud.get_users(db)
        return users
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_router.get("/me", response_model=UserSchema)
async def read_users_me(db: GetDBDep, current_user: GetCurrentUserDep) -> UserSchema:
    """Reads and returns the current user."""
    return current_user
