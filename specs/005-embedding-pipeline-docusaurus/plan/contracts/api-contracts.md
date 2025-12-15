# API Contracts for Embedding Pipeline

This section defines potential API contracts for the embedding pipeline system. While the current implementation is primarily a batch processing system, these contracts define potential future APIs for managing the pipeline.

## Current Pipeline API (Internal Functions)

The main.py file implements these internal function contracts:

### GET_ALL_URLS(sitemap_url) -> List[str]
- **Purpose**: Fetch all URLs from a sitemap
- **Input**: URL to sitemap XML
- **Output**: List of URLs to crawl

### EXTRACT_TEXT_FROM_URL(url) -> DocumentChunk
- **Purpose**: Extract clean text from a URL
- **Input**: URL to extract text from
- **Output**: DocumentChunk object with content and metadata

### CHUNK_TEXT(content, max_chunk_size, overlap) -> List[str]
- **Purpose**: Split content into chunks for embedding
- **Input**: Content string, maximum chunk size, overlap size
- **Output**: List of text chunks

### EMBED(text_chunk) -> EmbeddingVector
- **Purpose**: Generate embedding for text
- **Input**: Text chunk to embed
- **Output**: EmbeddingVector with vector data

### CREATE_COLLECTION(collection_name, vector_size) -> bool
- **Purpose**: Create Qdrant collection for storage
- **Input**: Name of collection and expected vector size
- **Output**: Success boolean

### SAVE_CHUNK_TO_QDRANT(chunk, embedding) -> bool
- **Purpose**: Store chunk and embedding in Qdrant
- **Input**: DocumentChunk and EmbeddingVector
- **Output**: Success boolean

## Future API Endpoints (Potential)

### GET /status
- **Purpose**: Get current status of indexing jobs
- **Response**: Indexing job status information

### POST /index
- **Purpose**: Trigger a new indexing job
- **Request Body**: 
  ```json
  {
    "sitemap_url": "https://example.com/sitemap.xml",
    "target_collection": "my_embeddings"
  }
  ```
- **Response**: Job ID and initial status

### GET /index/{job_id}
- **Purpose**: Get status of a specific indexing job
- **Response**: Detailed status information for the job

### POST /query
- **Purpose**: Query the vector database for similar content
- **Request Body**:
  ```json
  {
    "query_text": "What is robot kinematics?",
    "top_k": 5
  }
  ```
- **Response**: Relevant content chunks with metadata