from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from cruds import service_crud
from dependencies import GetDBDep, GetCurrentUserDep


service_router = APIRouter(prefix="/services", tags=["Service"])


@service_router.get("/")
async def read_services(db: GetDBDep, current_user: GetCurrentUserDep):
    services = service_crud.get_services(db)
    return services
