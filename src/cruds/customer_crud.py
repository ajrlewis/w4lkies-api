from datetime import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import distinct
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from exceptions import NotFoundError, DatabaseError
from models import User, Customer
from schemas.customer_schema import CustomerUpdateSchema, CustomerCreateSchema


def get_customers(db: SessionLocal, is_active: Optional[bool] = None) -> list[Customer]:
    query = db.query(Customer)
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    query = query.order_by(Customer.name)
    customers = query.all()
    return customers


def get_customer_by_id(db: SessionLocal, customer_id: int) -> Customer:
    customer = db.get(Customer, customer_id)
    logger.debug(f"{customer = }")
    logger.debug(f"{customer.email = }")
    if not customer:
        raise NotFoundError(f"Customer {customer_id} not found")
    return customer


def update_customer_by_id(
    db: SessionLocal,
    current_user: User,
    customer_id: int,
    customer_data: CustomerUpdateSchema,
) -> Customer:
    logger.debug(f"{current_user = } {customer_data = }")
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise NotFoundError(f"Customer {customer_id} not found")

    if name := customer_data.name:
        customer.name = name
    if phone := customer_data.phone:
        customer.phone = phone
    if email := customer_data.email:
        customer.email = email
    if emergency_contact_name := customer_data.emergency_contact_name:
        customer.emergency_contact_name = emergency_contact_name
    if emergency_contact_phone := customer_data.emergency_contact_phone:
        customer.emergency_contact_phone = emergency_contact_phone
    if is_active := customer_data.is_active:
        customer.is_active = is_active

    try:
        customer.updated_by = current_user.user_id
        db.commit()
        return customer
    except SQLAlchemyError as e:
        detail = f"Error updating customer: {e}"
        logger.error(detail)
        db.rollback()
        raise DatabaseError("An error occurred while updating the customer.")


def add_customer(
    db: SessionLocal, current_user: User, customer_data: CustomerCreateSchema
) -> Customer:
    logger.debug(f"{customer_data = }")
    customer = Customer(
        name=customer_data.name,
        phone=customer_data.phone,
        email=customer_data.email,
        emergency_contact_name=customer_data.emergency_contact_name,
        emergency_contact_phone=customer_data.emergency_contact_phone,
        is_active=customer_data.is_active,
        signed_up_on=datetime.utcnow(),
    )
    try:
        customer.created_by = current_user.user_id
        db.add(customer)
        db.commit()
        return customer
    except SQLAlchemyError as e:
        detail = f"Error adding customer: {e}"
        logger.error(detail)
        db.rollback()
        raise DatabaseError("An error occurred while adding a customer.")


def delete_customer_by_id(db: SessionLocal, customer_id: int):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise NotFoundError(f"customer {customer_id} not found")
    try:
        db.delete(customer)
        db.commit()
    except Exception as e:
        raise DatabaseError("An error occurred while deleting the customer.")
