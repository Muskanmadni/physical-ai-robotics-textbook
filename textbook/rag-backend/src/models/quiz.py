from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Quiz(BaseModel):
    id: str
    title: str
    chapterId: Optional[str] = None
    moduleId: Optional[str] = None
    questions: List[dict]  # List of question objects
    createdAt: datetime
    updatedAt: datetime

    class Config:
        alias_generator = lambda field: field
        allow_population_by_field_name = True