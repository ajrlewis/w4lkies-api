from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from cruds import invoice_crud
from dependencies import GetDBDep, GetCurrentUserDep


invoice_router = APIRouter(prefix="/invoices", tags=["invoice"])


@invoice_router.get("/")
async def read_invoices(db: GetDBDep, current_user: GetCurrentUserDep):
    invoices = invoice_crud.get_invoices(db)
    return invoices
