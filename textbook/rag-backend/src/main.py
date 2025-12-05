from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import auth, users, content, search, quizzes, progress, rag, personalization, translation

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="Backend API for the Physical AI & Humanoid Robotics textbook project",
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

# Include API routes
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(content.router, prefix="/api", tags=["Content"])
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(quizzes.router, prefix="/api", tags=["Quizzes"])
app.include_router(progress.router, prefix="/api", tags=["Progress"])
app.include_router(rag.router, prefix="/api", tags=["RAG"])
app.include_router(personalization.router, prefix="/api", tags=["Personalization"])
app.include_router(translation.router, prefix="/api", tags=["Translation"])

@app.get("/")
def read_root():
    return {"message": "Physical AI & Humanoid Robotics Textbook API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}