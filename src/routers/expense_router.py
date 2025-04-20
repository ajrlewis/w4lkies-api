from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from cruds import expense_crud
from dependencies import GetDBDep, GetCurrentUserDep


expense_router = APIRouter(prefix="/expenses", tags=["expense"])


@expense_router.get("/")
async def read_expenses(db: GetDBDep, current_user: GetCurrentUserDep):
    expenses = expense_crud.get_expenses(db)
    return expenses
