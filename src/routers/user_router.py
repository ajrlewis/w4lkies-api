from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger

from cruds import user_crud
from dependencies import GetDBDep, GetCurrentUserDep
from schemas import user_schema


user_router = APIRouter(prefix="/users", tags=["Users"])


# @user_router.post("/")
# async def create_user(db: GetDBDep, user: user_schema.UserCreate):
#     logger.debug(f"{user = }")
#     user = user_crud.create_user(db, user)
#     logger.debug(f"{db_user = }")
#     if user:
#         return db_user
#     else:
#         raise HTTPException(status_code=404, detail="user not added")


# user_id: Annotated[Union[int, None], Query(description="The user ID to fetch..")],
# response_model=user_schema.User
@user_router.get("/")
async def read_users(db: GetDBDep):
    users = user_crud.get_users(db, user_id)
    logger.debug(f"{db_user = }")
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=404, detail="user not added")


# @app.get("/me/", response_model=User)
@user_router.get("/me")
async def read_users_me(db: GetDBDep, current_user: GetCurrentUserDep):
    logger.debug(f"{db = }")
    logger.debug(f"{current_user = }")
    return current_user
