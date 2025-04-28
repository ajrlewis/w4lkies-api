from typing import Optional

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from exceptions import NotFoundError, DatabaseError
from models import User, Vet
from schemas.vet_schema import VetUpdateSchema, VetCreateSchema


def get_vets(db: SessionLocal) -> list[Vet]:
    query = db.query(Vet)
    query = query.order_by(Vet.name)
    vets = query.all()
    return vets


def get_vet_by_id(db: SessionLocal, vet_id: int) -> Vet:
    vet = db.get(Vet, vet_id)
    if not vet:
        raise NotFoundError(f"Vet {vet_id} not found")
    return vet


def update_vet_by_id(
    db: SessionLocal, current_user: User, vet_id: int, vet_data: VetUpdateSchema
) -> Vet:
    logger.debug(f"{current_user = } {vet_data = }")
    vet = get_vet_by_id(db, vet_id)
    if not vet:
        raise NotFoundError(f"Vet {vet_id} not found")

    if name := vet_data.name:
        vet.name = name
    if phone := vet_data.phone:
        vet.phone = phone
    if address := vet_data.address:
        vet.address = address

    try:
        vet.updated_by = current_user.user_id
        db.commit()
        return vet
    except SQLAlchemyError as e:
        detail = f"Error updating vet: {e}"
        logger.error(detail)
        db.rollback()
        raise DatabaseError("An error occurred while updating the vet.")


def add_vet(db: SessionLocal, current_user: User, vet_data: VetCreateSchema) -> Vet:
    logger.debug(f"{vet_data = }")
    vet = Vet(name=vet_data.name, address=vet_data.address, phone=vet_data.phone)
    try:
        vet.created_by = current_user.user_id
        db.add(vet)
        db.commit()
        return vet
    except SQLAlchemyError as e:
        detail = f"Error adding vet: {e}"
        logger.error(detail)
        db.rollback()
        raise DatabaseError("An error occurred while adding a vet.")


def delete_vet_by_id(db: SessionLocal, vet_id: int):
    vet = get_vet_by_id(db, vet_id)
    if not vet:
        raise NotFoundError(f"Vet {vet_id} not found")
    try:
        db.delete(vet)
        db.commit()
    except Exception as e:
        raise DatabaseError("An error occurred while deleting the vet.")
