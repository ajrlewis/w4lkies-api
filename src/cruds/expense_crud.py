from typing import Optional

from loguru import logger

from database import SessionLocal
from models import Expense


def get_expenses(db: SessionLocal) -> list[Expense]:
    return db.query(Expense).all()


def get_expense_by_id(db: SessionLocal, expense_id: int) -> Optional[Expense]:
    return db.query.get(Expense, expense_id)
