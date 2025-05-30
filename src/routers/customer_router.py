from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from loguru import logger

from cruds import customer_crud
from dependencies import GetDBDep, GetCurrentAdminUserDep
from exceptions import DatabaseError, NotFoundError
from schemas.customer_schema import (
    CustomerSchema,
    CustomerUpdateSchema,
    CustomerCreateSchema,
)

customer_router = APIRouter(prefix="/customers", tags=["Customers"])


@customer_router.get("/", response_model=list[CustomerSchema])
async def read_customers(
    db: GetDBDep,
    current_user: GetCurrentAdminUserDep,
    is_active: Optional[bool] = Query(
        None, description="Filter customers by their active status. Defaults to None."
    ),
) -> list[CustomerSchema]:
    """Reads and returns all customers from the database."""
    try:
        customers = customer_crud.get_customers(db, is_active=is_active)
        return customers
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@customer_router.get("/{customer_id}", response_model=CustomerSchema)
async def read_customer(
    db: GetDBDep, current_user: GetCurrentAdminUserDep, customer_id: int
) -> CustomerSchema:
    """Reads and returns a specific customer from the database."""
    try:
        customer = customer_crud.get_customer_by_id(db, customer_id)
        return customer
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@customer_router.put("/{customer_id}", response_model=CustomerSchema)
async def update_customer(
    db: GetDBDep,
    current_user: GetCurrentAdminUserDep,
    customer_id: int,
    customer_data: CustomerUpdateSchema,
) -> CustomerSchema:
    """Updates the properties of a specific customer in the database."""
    logger.debug(f"{customer_data = }")
    try:
        customer = customer_crud.update_customer_by_id(
            db, current_user, customer_id, customer_data
        )
        return customer
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@customer_router.delete("/{customer_id}")
async def delete_customer(
    db: GetDBDep, current_user: GetCurrentAdminUserDep, customer_id: int
):
    """Deletes a specific customer in the database."""
    try:
        customer = customer_crud.delete_customer_by_id(db, customer_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@customer_router.post("/", response_model=CustomerSchema)
async def create_customer(
    db: GetDBDep,
    current_user: GetCurrentAdminUserDep,
    customer_data: CustomerCreateSchema,
) -> CustomerSchema:
    """Creates a customer to add to the database."""
    try:
        customer = customer_crud.add_customer(db, current_user, customer_data)
        return customer
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
