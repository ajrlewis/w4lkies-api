from typing import Optional

from loguru import logger

from database import SessionLocal
from models import Booking


def get_bookings(db: SessionLocal) -> list[Booking]:
    return db.query(Booking).all()


def get_booking_by_id(db: SessionLocal, booking_id: int) -> Optional[Booking]:
    return db.query.get(Booking, booking_id)
