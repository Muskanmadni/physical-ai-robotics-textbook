from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Chapter(BaseModel):
    id: str
    title: str
    content: str
    module: str
    order: int
    language: str = "en"
    createdAt: datetime
    updatedAt: datetime
    metadata: Optional[dict] = None

    class Config:
        alias_generator = lambda field: field
        allow_population_by_field_name = True