from pydantic import BaseModel
from datetime import datetime

class Translation(BaseModel):
    id: str
    originalContentId: str  # Can reference Chapter, Quiz, etc.
    originalContentType: str  # "Chapter", "Quiz", etc.
    language: str
    translatedContent: dict  # JSON object with translated content
    createdAt: datetime
    updatedAt: datetime

    class Config:
        alias_generator = lambda field: field
        allow_population_by_field_name = True