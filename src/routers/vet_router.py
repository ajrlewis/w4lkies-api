from typing import Annotated, Any, Optional, Union

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from cruds import vet_crud
from dependencies import GetDBDep, GetCurrentAdminUserDep
from exceptions import DatabaseError, NotFoundError
from schemas.vet_schema import VetSchema, VetUpdateSchema, VetCreateSchema

vet_router = APIRouter(prefix="/vets", tags=["Vets"])


@vet_router.get("/", response_model=list[VetSchema])
async def read_vets(db: GetDBDep) -> Any:
    vets = vet_crud.get_vets(db)
    return vets


@vet_router.get("/{vet_id}", response_model=VetSchema)
async def read_vet(db: GetDBDep, vet_id: int) -> VetSchema:
    vet = vet_crud.get_vet_by_id(db, vet_id)
    logger.debug(f"{vet = }")
    if vet:
        return vet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vet {vet_id} not found"
        )


@vet_router.put("/{vet_id}", response_model=Optional[VetSchema])
async def update_vet(
    db: GetDBDep,
    current_user: GetCurrentAdminUserDep,
    vet_id: int,
    vet_data: VetUpdateSchema,
) -> Optional[VetSchema]:
    logger.debug(f"{vet_data = }")
    try:
        vet = vet_crud.update_vet_by_id(db, current_user, vet_id, vet_data)
        return vet
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


@vet_router.delete("/{vet_id}")
async def delete_vet(db: GetDBDep, current_user: GetCurrentAdminUserDep, vet_id: int):
    try:
        vet = vet_crud.delete_vet_by_id(db, vet_id)
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


@vet_router.post("/", response_model=VetSchema)
async def create_vet(
    db: GetDBDep, current_user: GetCurrentAdminUserDep, vet_data: VetCreateSchema
) -> VetSchema:
    try:
        vet = vet_crud.add_vet(db, current_user, vet_data)
        return vet
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
