import secrets
from typing import Optional

import bcrypt
from loguru import logger

from database import SessionLocal
from models import User


def get_user_by_name(db: SessionLocal, name: str) -> Optional[User]:
    return db.query(User).filter_by(name=name).first()
