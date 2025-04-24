from typing import Union

from pydantic import BaseModel


class ContactUs(BaseModel):
    name: str
    email: str
    message: str
