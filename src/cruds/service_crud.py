from typing import Optional

from loguru import logger
from sqlalchemy import distinct
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from exceptions import NotFoundError, DatabaseError
from models import User, Service
from schemas.service_schema import ServiceUpdateSchema, ServiceCreateSchema


def get_services(
    db: SessionLocal,
    is_active: Optional[bool] = None,
    is_publicly_offered: Optional[bool] = None,
) -> list[Service]:
    query = db.query(Service)
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    if is_publicly_offered is not None:
        query = query.filter_by(is_publicly_offered=is_publicly_offered)
    query = query.order_by(Service.name)
    services = query.all()
    return services


def get_service_by_id(db: SessionLocal, service_id: int) -> Service:
    service = db.get(Service, service_id)
    if not service:
        raise NotFoundError(f"Service {service_id} not found")
    return service


def update_service_by_id(
    db: SessionLocal,
    current_user: User,
    service_id: int,
    service_data: ServiceUpdateSchema,
) -> Service:
    logger.debug(f"{current_user = } {service_data = }")
    service = get_service_by_id(db, service_id)
    if not service:
        raise NotFoundError(f"Service {service_id} not found")

    if name := service_data.name:
        service.name = name
    if price := service_data.price:
        service.price = price
    if description := service_data.description:
        service.description = description
    if duration := service_data.duration:
        service.duration = duration
    is_publicly_offered = service_data.is_publicly_offered
    if is_publicly_offered is not None:
        service.is_publicly_offered = is_publicly_offered
    is_active = service_data.is_active
    if is_active is not None:
        service.is_active = is_active

    try:
        service.updated_by = current_user.user_id
        db.commit()
        return service
    except SQLAlchemyError as e:
        detail = f"Error updating service: {e}"
        logger.error(detail)
        db.rollback()
        raise DatabaseError("An error occurred while updating the service.")


def add_service(
    db: SessionLocal, current_user: User, service_data: ServiceCreateSchema
) -> Service:
    logger.debug(f"{service_data = }")
    service = Service(
        name=service_data.name,
        price=service_data.price,
        description=service_data.description,
        duration=service_data.duration,
        is_publicly_offered=service_data.is_publicly_offered,
        is_active=service_data.is_active,
    )
    try:
        service.created_by = current_user.user_id
        db.add(service)
        db.commit()
        return service
    except SQLAlchemyError as e:
        detail = f"Error adding service: {e}"
        logger.error(detail)
        db.rollback()
        raise DatabaseError("An error occurred while adding a service.")


def delete_service_by_id(db: SessionLocal, service_id: int):
    service = get_service_by_id(db, service_id)
    if not service:
        raise NotFoundError(f"Service {service_id} not found")
    try:
        db.delete(service)
        db.commit()
    except Exception as e:
        raise DatabaseError("An error occurred while deleting the service.")
