from pydantic import BaseModel
from datetime import datetime
from typing import List

class RAGDocument(BaseModel):
    id: str
    chapterId: str
    content: str
    embedding: List[float]  # Vector embedding
    vectorId: str  # Reference to Qdrant
    createdAt: datetime
    updatedAt: datetime

    class Config:
        alias_generator = lambda field: field
        allow_population_by_field_name = True