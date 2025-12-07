from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.rag_router import router as rag_router
from .api.health_router import router as health_router

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)