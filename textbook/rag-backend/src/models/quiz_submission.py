from pydantic import BaseModel
from datetime import datetime
from typing import List

class QuizSubmission(BaseModel):
    id: str
    quizId: str
    userId: str
    answers: List[dict]  # List of answer objects
    score: int  # Percentage score
    completedAt: datetime
    createdAt: datetime

    class Config:
        alias_generator = lambda field: field
        allow_population_by_field_name = True