from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PersonalizedContent(BaseModel):
    id: str
    originalChapterId: str
    userId: str
    personalizedContent: str
    personalizationType: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        alias_generator = lambda field: field
        allow_population_by_field_name = True