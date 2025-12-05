# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.11 or higher)
- Git
- Access to Neon PostgreSQL and Qdrant cloud accounts (for free tier)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd physical-ai-humanoid-robotics-textbook
```

### 2. Frontend Setup (Docusaurus)

```bash
# Navigate to the textbook directory
cd textbook

# Install dependencies
npm install

# Set environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Backend Setup (FastAPI)

```bash
# Navigate to the rag-backend directory
cd rag-backend

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration for:
# - Neon PostgreSQL connection
# - Qdrant vector database
# - Better-Auth secrets
```

### 4. Environment Configuration

Create a `.env` file in both the frontend and backend with the following variables:

**Backend (.env):**
```
DATABASE_URL=your_neon_postgresql_connection_string
QDRANT_URL=your_qdrant_connection_string
QDRANT_API_KEY=your_qdrant_api_key
AUTH_SECRET=your_auth_secret
```

## Running the Application

### 1. Start the Backend

```bash
cd rag-backend
python -m uvicorn src.main:app --reload --port 8000
```

### 2. Start the Frontend

```bash
cd textbook  # or wherever Docusaurus is set up
npm start
```

The application will be available at `http://localhost:3000`.

## Building for Production

### Frontend Build

```bash
cd textbook
npm run build
```

### Deploying to GitHub Pages

```bash
npm run deploy
```

## API Documentation

The backend API documentation is available at `http://localhost:8000/docs` when the server is running.