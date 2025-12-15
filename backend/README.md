# Embedding Pipeline Backend

This backend service extracts text from deployed Docusaurus URLs, generates embeddings using Cohere, and stores them in Qdrant for RAG-based retrieval. The service is built with FastAPI and can run as both a batch job and a REST API.

## Overview

The system:
- Crawls a deployed Docusaurus site using its sitemap
- Extracts clean text from each page
- Chunks the text into manageable pieces
- Generates embeddings using the Cohere API
- Stores embeddings in Qdrant with metadata for retrieval
- Provides a REST API for indexing and querying operations

## Requirements

- Python 3.9+
- UV package manager
- Cohere API key
- Qdrant instance (local or cloud)

## Setup

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   TARGET_SITE_URL=https://physical-ai-robotics-textbook-three.vercel.app/
   SITEMAP_URL=https://physical-ai-robotics-textbook-three.vercel.app/sitemap.xml
   ```

## Usage

### Running as a Web Service (FastAPI)
```bash
python main.py
```
This will start a FastAPI server on `http://localhost:8000` with the following endpoints:
- `GET /` - API status check
- `POST /index` - Start an indexing job
- `GET /status/{job_id}` - Get status of an indexing job
- `POST /query` - Query the vector database for similar content
- `GET /collections` - List all Qdrant collections

### Running as a Batch Job
```bash
python main.py
```
This will run the pipeline as a batch process using the default configuration.

## API Endpoints

### `POST /index`
Start an indexing job to process documentation from a sitemap.
Request body:
```json
{
  "sitemap_url": "https://example.com/sitemap.xml",
  "collection_name": "rag_embeddings"
}
```

### `GET /status/{job_id}`
Get the status of an indexing job.

### `POST /query`
Query the vector database for similar content.
Request body:
```json
{
  "query_text": "What is robot kinematics?",
  "top_k": 5
}
```

### `GET /collections`
List all Qdrant collections.

## Architecture

The system consists of the following components:

- `get_all_urls()`: Fetches all URLs from the sitemap
- `extract_text_from_url()`: Extracts clean text from each URL
- `chunk_text()`: Splits text into appropriately sized chunks
- `embed()`: Generates embeddings using Cohere
- `create_collection()`: Sets up Qdrant collection
- `save_chunk_to_qdrant()`: Stores embeddings with metadata in Qdrant
- `main()`: Orchestrates the entire pipeline
- FastAPI endpoints: Expose functionality as REST API

## Configuration

The system is configured through environment variables in the `.env` file:

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL for your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant access
- `TARGET_SITE_URL`: Base URL of the Docusaurus site to index
- `SITEMAP_URL`: URL to the site's sitemap.xml file

## Data Model

The system uses the following key data structures:

- **DocumentChunk**: Represents a segment of documentation content with metadata
- **EmbeddingVector**: The numerical representation of text content
- **IndexingJob**: Tracks the progress of a full indexing run

## Error Handling

The system includes robust error handling:
- Network request retries with exponential backoff
- Cohere API rate limit handling
- Database connection recovery strategies
- Progress tracking to allow resumption after failures
- Structured logging for all pipeline stages

## Deploying to Render

This application uses a Dockerfile to handle deployment to Render, which resolves potential Rust compilation issues that may occur during package installation.

### Known Issue Resolution

If you encounter the following error during deployment:

```
Preparing metadata (pyproject.toml): finished with status 'error'
error: subprocess-exited-with-error
× Preparing metadata (pyproject.toml) did not run successfully.
│ exit code: 1
╰─> [14 lines of output]
        Updating crates.io index
    warning: failed to write cache, path: /usr/local/cargo/registry/index/index.crates.io-1949cf8c6b5b557f/.cache/ah/as/ahash, error: Read-only file system (os error 30)
     Downloading crates ...
      Downloaded cfg-if v1.0.0
    error: failed to create directory `/usr/local/cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`

    Caused by:
      Read-only file system (os error 30)
```

This is caused by certain Python packages (like those with Rust dependencies) attempting to compile during installation. Our Dockerfile addresses this by:

1. Installing system dependencies needed for compilation
2. Using a Docker container with the necessary tools available
3. Upgrading pip to use the latest installation methods

## Local Development

To run locally:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
uvicorn main:app --reload --port 8000
```

## Environment Variables

Create a `.env` file with the following variables:

```
GEMINI_API_KEY=your_google_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
TARGET_SITE_URL=https://physical-ai-robotics-textbook-three.vercel.app/
SITEMAP_URL=https://physical-ai-robotics-textbook-three.vercel.app/sitemap.xml
```
