from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Module(BaseModel):
    id: str
    title: str
    description: str
    order: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        alias_generator = lambda field: field
        allow_population_by_field_name = True