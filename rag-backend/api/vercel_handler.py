import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.rag_router import router as rag_router
from src.api.health_router import router as health_router
from mangum import Mangum

# Create FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics RAG API",
    description="API for the RAG system connected with the Physical AI & Humanoid Robotics textbook",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(rag_router, prefix="/api", tags=["rag"])

# Create Mangum handler for ASGI compatibility
handler = Mangum(app)

# For Vercel compatibility
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))