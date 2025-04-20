from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from cruds import dog_crud
from dependencies import GetDBDep, GetCurrentUserDep


dog_router = APIRouter(prefix="/dogs", tags=["Dog"])


@dog_router.get("/")
async def read_dogs(db: GetDBDep, current_user: GetCurrentUserDep):
    dogs = dog_crud.get_dogs(db)
    return dogs
