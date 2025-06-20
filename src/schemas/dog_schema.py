from typing import List, Optional, Union
from datetime import datetime

from pydantic import BaseModel, create_model

from schemas.customer_schema import CustomerBaseSchema
from schemas.vet_schema import VetBaseSchema


class DogBaseSchema(BaseModel):
    name: str
    date_of_birth: Union[datetime, None] = None
    breed: str
    is_allowed_treats: bool
    is_allowed_off_the_lead: bool
    is_allowed_on_social_media: bool
    is_neutered_or_spayed: bool
    behavioral_issues: str = ""
    medical_needs: str = ""
    # customer_id: int = 0
    customer: CustomerBaseSchema
    # vet_id: int = 0
    vet: VetBaseSchema


fields = {
    field: DogBaseSchema.__annotations__[field]
    for field in DogBaseSchema.__annotations__
    if field not in {"customer_id", "vet_id", "customer", "vet"}
}
fields["customer_id"] = int
fields["vet_id"] = int
DogCreateSchema = create_model("DogCreateSchema", **fields)


# class DogCreateSchema(DogBaseSchema):
#     pass


class DogUpdateSchema(BaseModel):
    name: Union[str, None] = None
    date_of_birth: datetime
    breed: Union[str, None] = None
    is_allowed_treats: Union[bool, None] = None
    is_allowed_off_the_lead: Union[bool, None] = None
    is_allowed_on_social_media: Union[bool, None] = None
    is_neutered_or_spayed: Union[bool, None] = None
    behavioral_issues: Union[str, None] = None
    medical_needs: Union[str, None] = None
    customer_id: Union[int, None] = None
    vet_id: Union[int, None] = None


class DogSchema(DogBaseSchema):
    dog_id: int

    class Config:
        from_attributes = True
