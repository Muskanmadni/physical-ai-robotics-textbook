from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str = "healthy"
    message: str = "RAG API is running"

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse()