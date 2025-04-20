from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from cruds import vet_crud
from dependencies import GetDBDep, GetCurrentUserDep


vet_router = APIRouter(prefix="/vets", tags=["Vet"])


@vet_router.get("/")
async def read_vets(db: GetDBDep, current_user: GetCurrentUserDep):
    vets = vet_crud.get_vets(db)
    return vets
