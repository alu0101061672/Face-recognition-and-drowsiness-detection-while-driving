from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class Vehicle(BaseModel):
    _id: Optional[UUID] = uuid4()
    brand: str
    serial_number: str
    driver_id: Optional[UUID]
    digital_key: dict
    purchased_at: datetime = datetime.now()