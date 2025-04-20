from typing import Optional

from loguru import logger

from database import SessionLocal
from models import Service


def get_services(db: SessionLocal) -> list[Service]:
    return db.query(Service).all()


def get_service_by_id(db: SessionLocal, service_id: int) -> Optional[Service]:
    return db.query.get(Service, service_id)
