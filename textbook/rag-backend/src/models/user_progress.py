from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserProgress(BaseModel):
    id: str
    userId: str
    chapterId: str
    completed: bool = False
    progressPercentage: int = 0
    lastAccessed: datetime
    createdAt: datetime
    updatedAt: datetime

    class Config:
        alias_generator = lambda field: field
        allow_population_by_field_name = True