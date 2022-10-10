from typing import Optional
from pydantic import BaseModel
from datetime import date, timedelta
from typing import Optional
from uuid import UUID, uuid4
from models.driver import *

class Type(str, Enum):
    am = "AM",
    a1 = "A1",
    a2 = "A2",
    a = "A",
    b = "B",
    be = "B+E",
    c1 = "C1",
    ce = "C+E",
    d1 = "D1",
    d1e = "D1+E",
    d = "D"
    de = "D+E"

class License(BaseModel):
    _id: Optional[UUID] = uuid4()
    type: Type
    points: int
    driver_id: Optional[UUID]
    expiration_date: date