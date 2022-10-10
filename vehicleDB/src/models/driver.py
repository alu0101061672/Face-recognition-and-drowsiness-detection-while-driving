from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class SchemaDriver(BaseModel):
    _id: Optional[UUID] = uuid4()
    full_name: str
    dni: str
    facial_embedding: Optional[list]
    created_at: Optional[datetime] = datetime.now()

class UpdateDriverModel(BaseModel):
    _id: Optional[UUID] = uuid4()
    full_name: Optional[str]
    dni: Optional[str]
    facial_embedding: Optional[list]
    created_at: Optional[datetime] = datetime.now()

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}