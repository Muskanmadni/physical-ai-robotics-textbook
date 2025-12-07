from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class RAGDocument(BaseModel):
    id: str
    chapterId: str
    content: str
    embedding: List[float]
    vectorId: str
    createdAt: datetime
    updatedAt: datetime


class RAGQueryRequest(BaseModel):
    query: str
    userId: Optional[str] = None


class RAGSource(BaseModel):
    chapterId: str
    title: str
    relevance: float


class RAGQueryResponse(BaseModel):
    response: str
    sources: List[RAGSource]