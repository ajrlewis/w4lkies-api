from typing import Optional

from loguru import logger

from database import SessionLocal
from models import Invoice


def get_invoices(db: SessionLocal) -> list[Invoice]:
    return db.query(Invoice).all()


def get_invoice_by_id(db: SessionLocal, invoice_id: int) -> Optional[Invoice]:
    return db.query.get(Invoice, invoice_id)
