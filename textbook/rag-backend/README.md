# Physical AI & Humanoid Robotics Backend

This is the backend API for the Physical AI & Humanoid Robotics textbook project, providing services for content delivery, user management, personalization, and RAG (Retrieval-Augmented Generation) features.

## Features

- User authentication and management
- Textbook content delivery
- Personalized learning paths
- Multilingual support (English/Urdu)
- RAG-powered search and Q&A
- Progress tracking
- Quiz and assessment systems

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- Qdrant (vector database)
- Neon PostgreSQL (metadata storage)
- Sentence Transformers (for embeddings)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the development server:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Documentation

The API documentation is available at `/docs` when the server is running.

## Endpoints

- `/api/auth` - Authentication endpoints
- `/api/users` - User management
- `/api/modules` - Module listings and details
- `/api/chapters/{id}` - Chapter content
- `/api/search` - Textbook search functionality
- `/api/rag/query` - RAG-powered queries
- `/api/quizzes/{id}` - Quiz management
- `/api/users/progress` - Learning progress tracking
- `/api/translate/{id}` - Translation endpoints

## Environment Variables

- `DATABASE_URL`: Database connection string
- `QDRANT_URL`: Qdrant vector database URL
- `QDRANT_API_KEY`: Qdrant API key
- `AUTH_SECRET`: Secret key for JWT tokens
- `BACKEND_CORS_ORIGINS`: Allowed origins for CORS

## License

This project is licensed under the MIT License - see the LICENSE file for details.