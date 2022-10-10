from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

class Gender(str, Enum):
    male = "male",
    female = "female"

class Driver(BaseModel):
    _id: Optional[UUID] = uuid4()
    full_name: str
    gender: Gender
    dni: str
    address: str
    facial_embedding: list 
    infractions: Optional[list[str]]
    created_at: datetime