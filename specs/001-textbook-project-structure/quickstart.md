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

**Frontend (.env):**
```
BACKEND_API_URL=http://localhost:8000
AUTH_PROVIDER=your_auth_provider
```

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
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 2. Start the Frontend

```bash
cd textbook  # or wherever Docusaurus is set up
npm start
```

The application will be available at `http://localhost:3000`.

## Development Workflow

### Adding New Chapters

1. Create a new markdown file in `docs/chapters/`
2. Add an entry to `sidebars.js` to include it in navigation
3. Ensure the file follows the Docusaurus document format

### Working with RAG Features

1. To add content to the vector database:
   - Add your content to the appropriate chapter files
   - Run the embedding pipeline: `python scripts/embed_content.py`
   - The system will generate embeddings and store them in Qdrant

### Database Migrations

```bash
# Run backend in development mode
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Testing

### Frontend Tests

```bash
cd textbook
npm test
# or for continuous testing
npm run test:watch
```

### Backend Tests

```bash
cd backend
python -m pytest
```

### End-to-End Tests

```bash
# Make sure both frontend and backend are running first
npm run test:e2e
```

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

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify your Neon PostgreSQL connection string is correct
   - Ensure your IP is whitelisted in Neon console

2. **Vector Database Connection Errors**
   - Check your Qdrant URL and API key
   - Verify network access to Qdrant cloud

3. **Authentication Issues**
   - Ensure your AUTH_SECRET is the same in both frontend and backend
   - Check that Better-Auth is configured correctly

4. **Docusaurus Build Errors**
   - Clear the cache: `npx docusaurus clear`
   - Reinstall dependencies: `rm -rf node_modules && npm install`

## Next Steps

1. Review the API contracts in `specs/001-textbook-project-structure/contracts/` to understand the backend interface
2. Check the data model in `specs/001-textbook-project-structure/data-model.md` for database schema details
3. Explore the research findings in `specs/001-textbook-project-structure/research.md` for architecture insights
4. Look at the implementation plan in `specs/001-textbook-project-structure/plan.md` for the project roadmap