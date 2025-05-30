from typing import Optional

from loguru import logger
from sqlalchemy import distinct
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from exceptions import NotFoundError, DatabaseError
from models import User, Customer, Dog, Vet
from schemas.dog_schema import DogUpdateSchema, DogCreateSchema


def get_dogs(db: SessionLocal) -> list[Dog]:
    query = db.query(Dog)
    query = query.order_by(Dog.name)
    dogs = query.all()
    return dogs


def get_dog_breeds(db: SessionLocal) -> list[str]:
    query = db.query(distinct(Dog.breed))
    query = query.order_by(Dog.breed)
    results = query.all()
    logger.debug(f"{results = }")
    dog_breeds = [result[0] for result in results]
    logger.debug(f"{dog_breeds = }")
    return dog_breeds


def get_dog_by_id(db: SessionLocal, dog_id: int) -> Dog:
    dog = db.get(Dog, dog_id)
    if not dog:
        raise NotFoundError(f"Dog {dog_id} not found")
    return dog


def update_dog_by_id(
    db: SessionLocal, current_user: User, dog_id: int, dog_data: DogUpdateSchema
) -> Dog:
    logger.debug(f"{current_user = } {dog_data = }")
    dog = get_dog_by_id(db, dog_id)
    if not dog:
        raise NotFoundError(f"Dog {dog_id} not found")

    if name := dog_data.name:
        dog.name = name
    if date_of_birth := dog_data.date_of_birth:
        dog.date_of_birth = date_of_birth
    if is_allowed_treats := dog_data.is_allowed_treats:
        dog.is_allowed_treats = is_allowed_treats
    if is_allowed_off_the_lead := dog_data.is_allowed_off_the_lead:
        dog.is_allowed_off_the_lead = is_allowed_off_the_lead
    if is_allowed_on_social_media := dog_data.is_allowed_on_social_media:
        dog.is_allowed_on_social_media = is_allowed_on_social_media
    if is_neutered_or_spayed := dog_data.is_neutered_or_spayed:
        dog.is_neutered_or_spayed = is_neutered_or_spayed
    if behavioral_issues := dog_data.behavioral_issues:
        dog.behavioral_issues = behavioral_issues
    if medical_needs := dog_data.medical_needs:
        dog.medical_needs = medical_needs
    if breed := dog_data.breed:
        dog.breed = breed
    if customer_id := dog_data.customer_id:
        dog.customer_id = customer_id
    if vet_id := dog_data.vet_id:
        dog.vet_id = vet_id

    try:
        dog.updated_by = current_user.user_id
        db.commit()
        return dog
    except SQLAlchemyError as e:
        detail = f"Error updating dog: {e}"
        logger.error(detail)
        db.rollback()
        raise DatabaseError("An error occurred while updating the dog.")


def add_dog(db: SessionLocal, current_user: User, dog_data: DogCreateSchema) -> Dog:
    logger.debug(f"{dog_data = }")
    dog = Dog(
        name=dog_data.name,
        date_of_birth=dog_data.date_of_birth,
        is_allowed_treats=dog_data.is_allowed_treats,
        is_allowed_off_the_lead=dog_data.is_allowed_off_the_lead,
        is_allowed_on_social_media=dog_data.is_allowed_on_social_media,
        is_neutered_or_spayed=dog_data.is_neutered_or_spayed,
        behavioral_issues=dog_data.behavioral_issues,
        medical_needs=dog_data.medical_needs,
        breed=dog_data.breed,
        customer_id=dog_data.customer_id,
        vet_id=dog_data.vet_id,
    )
    try:
        dog.created_by = current_user.user_id
        db.add(dog)
        db.commit()
        return dog
    except SQLAlchemyError as e:
        detail = f"Error adding dog: {e}"
        logger.error(detail)
        db.rollback()
        raise DatabaseError("An error occurred while adding a dog.")


def delete_dog_by_id(db: SessionLocal, dog_id: int):
    dog = get_dog_by_id(db, dog_id)
    if not dog:
        raise NotFoundError(f"Dog {dog_id} not found")
    try:
        db.delete(dog)
        db.commit()
    except Exception as e:
        raise DatabaseError("An error occurred while deleting the dog.")
