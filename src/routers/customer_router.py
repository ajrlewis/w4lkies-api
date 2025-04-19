from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from cruds import customer_crud
from dependencies import GetDBDep, GetCurrentUserDep

# from schemas.customer_schema import CustomerSchema
from services import customer_service


customer_router = APIRouter(prefix="/customer", tags=["Customer"])


@customer_router.get("/")
async def read_customers(db: GetDBDep, current_user: GetCurrentUserDep):
    customers = customer_crud.get_customers(db)
    return customers


# @customer_router.get("/{customer_id}")
# async def read_customer(db: GetDBDep, customer_id: int):
#     if item_id not in fake_items_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
#         )
#     return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
