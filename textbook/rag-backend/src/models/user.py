from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str
    email: str
    name: str
    preferences: Optional[dict] = None
    createdAt: datetime
    updatedAt: datetime
    authProvider: Optional[str] = None
    profilePicture: Optional[str] = None

    class Config:
        # This allows the model to be converted to dict with lowercase field names
        alias_generator = lambda field: field
        allow_population_by_field_name = True