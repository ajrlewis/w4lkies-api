from typing import List, Optional, Union
from datetime import datetime, time

from pydantic import BaseModel

from schemas.customer_schema import CustomerSchema, CustomerSnippetSchema
from schemas.service_schema import ServiceSchema, ServiceSnippetSchema
from schemas.user_schema import UserSnippetSchema


class BookingSnippetSchema(BaseModel):
    booking_id: int
    date: datetime
    time: time
    customer: CustomerSnippetSchema
    service: ServiceSnippetSchema
    user: UserSnippetSchema


class BookingBaseSchema(BaseModel):
    date: datetime
    time: time
    customer: CustomerSchema
    service: ServiceSchema
    user_id: int


class BookingCreateSchema(BaseModel):
    date: datetime
    time: time
    customer_id: int
    service_id: int
    user_id: int


class BookingUpdateSchema(BaseModel):
    date: Union[datetime, None] = None
    time: Union[time, None] = None
    customer_id: Union[int, None] = None
    service_id: Union[int, None] = None
    user_id: Union[int, None] = None


class BookingSchema(BookingBaseSchema):
    booking_id: int

    class Config:
        from_attributes = True
