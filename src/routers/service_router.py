from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from loguru import logger

from cruds import service_crud
from dependencies import GetDBDep, GetCurrentAdminUserDep
from exceptions import DatabaseError, NotFoundError
from schemas.service_schema import (
    ServiceSchema,
    ServiceUpdateSchema,
    ServiceCreateSchema,
)

service_router = APIRouter(prefix="/services", tags=["Services"])


@service_router.get("/", response_model=list[ServiceSchema])
async def read_services(
    db: GetDBDep,
    is_active: Optional[bool] = Query(
        None, description="Filter services by their active status. Defaults to None."
    ),
    is_publicly_offered: Optional[bool] = Query(
        None,
        description="Filter services by their public availability. Defaults to None.",
    ),
) -> list[ServiceSchema]:
    """Reads and returns all services from the database."""
    try:
        services = service_crud.get_services(
            db, is_active=is_active, is_publicly_offered=is_publicly_offered
        )
        return services
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@service_router.get("/{service_id}", response_model=ServiceSchema)
async def read_service(db: GetDBDep, service_id: int) -> ServiceSchema:
    """Reads and returns a specific service from the database."""
    try:
        service = service_crud.get_service_by_id(db, service_id)
        return service
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@service_router.put("/{service_id}", response_model=ServiceSchema)
async def update_service(
    db: GetDBDep,
    current_user: GetCurrentAdminUserDep,
    service_id: int,
    service_data: ServiceUpdateSchema,
) -> ServiceSchema:
    """Updates the properties of a specific service in the database."""
    logger.debug(f"{service_data = }")
    try:
        service = service_crud.update_service_by_id(
            db, current_user, service_id, service_data
        )
        return service
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


@service_router.delete("/{service_id}")
async def delete_service(
    db: GetDBDep, current_user: GetCurrentAdminUserDep, service_id: int
):
    """Deletes a specific service in the database."""
    try:
        service = service_crud.delete_service_by_id(db, service_id)
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


@service_router.post("/", response_model=ServiceSchema)
async def create_service(
    db: GetDBDep,
    current_user: GetCurrentAdminUserDep,
    service_data: ServiceCreateSchema,
) -> ServiceSchema:
    """Creates a service to add to the database."""
    try:
        service = service_crud.add_service(db, current_user, service_data)
        return service
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
