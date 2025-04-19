from typing import Optional

from loguru import logger

from database import SessionLocal
from models import Customer


def get_customers(db: SessionLocal) -> list[Customer]:
    return db.query(Customer).all()


def get_customer_by_id(db: SessionLocal, customer_id: int) -> Optional[Customer]:
    return db.query.get(Customer, customer_id)
