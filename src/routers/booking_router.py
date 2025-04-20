from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from cruds import booking_crud
from dependencies import GetDBDep, GetCurrentUserDep


booking_router = APIRouter(prefix="/bookings", tags=["booking"])


@booking_router.get("/")
async def read_bookings(db: GetDBDep, current_user: GetCurrentUserDep):
    bookings = booking_crud.get_bookings(db)
    return bookings
