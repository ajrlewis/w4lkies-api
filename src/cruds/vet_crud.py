from typing import Optional

from loguru import logger

from database import SessionLocal
from models import Vet


def get_vets(db: SessionLocal) -> list[Vet]:
    return db.query(Vet).all()


def get_vet_by_id(db: SessionLocal, vet_id: int) -> Optional[Vet]:
    return db.query.get(Vet, vet_id)
