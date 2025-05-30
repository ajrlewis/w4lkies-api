import secrets
from typing import Optional

import bcrypt
from loguru import logger

from database import SessionLocal
from models import User


def get_users(db: SessionLocal, is_active: Optional[bool] = None) -> list[User]:
    query = db.query(User)
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    users = query.all()
    return users


def get_user_by_name(db: SessionLocal, name: str) -> Optional[User]:
    return db.query(User).filter_by(name=name).first()
