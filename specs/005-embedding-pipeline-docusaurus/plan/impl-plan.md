# Implementation Plan: Embedding Pipeline for Documentation Retrieval

**Feature**: 005-embedding-pipeline-docusaurus
**Created**: 2025-12-15
**Status**: Draft
**Author**: Assistant

## Technical Context

The system needs to extract text from deployed Docusaurus URLs, generate embeddings using Cohere, and store them in Qdrant for RAG-based retrieval.

This will be a backend service written in Python using the following technologies:
- **Package Manager**: UV (for fast dependency management)
- **Cohere Client**: For generating text embeddings
- **Qdrant Client**: For vector storage and retrieval
- **BeautifulSoup**: For HTML parsing and content extraction
- **Requests**: For HTTP requests to fetch web pages

### System Architecture

The system design will follow these steps:
1. Fetch and parse the sitemap to get all URLs
2. Extract text from each URL
3. Clean and chunk the text
4. Generate embeddings using Cohere
5. Store embeddings in Qdrant with metadata

### Dependencies

- Python 3.9+
- Cohere Python library
- Qdrant Python library
- BeautifulSoup4
- Requests
- python-dotenv (for environment variable management)

### Deployment Link

- Target site: https://physical-ai-robotics-textbook-three.vercel.app/
- Sitemap: https://physical-ai-robotics-textbook-three.vercel.app/sitemap.xml

## Constitution Check

### Interdisciplinary Collaboration
- The system will provide access to comprehensive robotics and AI documentation, fostering interdisciplinary knowledge sharing.

### Ethical AI Development
- The system will only index publicly available documentation, respecting content ownership and access controls.

### Robustness & Safety Engineering
- The system will include error handling for network requests, API calls, and data processing failures.
- Rate limiting will be implemented to avoid overloading target servers.

### Human–Robot Interaction (HRI) Design
- While this is a backend system, it will enable better documentation access, which supports HRI design principles.

### Continuous Learning & Adaptation
- The system will allow for updating embeddings as documentation changes, supporting continuous learning.

### Technical Standards
- The system will follow clean code principles and proper error handling.
- Standardized interfaces will be used for all external services (Cohere, Qdrant).

## Gates

### Technical Feasibility ✅
- All required technologies (Cohere API, Qdrant, Python libraries) are readily available
- The target website has a sitemap for crawling

### Resource Availability ✅
- Cohere API access and tokens can be obtained
- Qdrant vector database can be set up (cloud or local instance)
- Python development environment is standard

### Compliance ✅
- System only accesses public documentation
- Proper rate limiting will be implemented to respect server resources
- No personal data is processed

## Phase 0: Outline & Research

### Research Tasks

#### RT-001: Determine Optimal Text Chunking Strategy
- **Decision**: Chunk size and overlap strategy for embedding generation
- **Rationale**: Cohere has token limits that affect how we chunk text. Need to find optimal size for semantic coherence while maximizing token usage.
- **Alternatives considered**: Fixed-size chunks vs. semantic boundary chunks

#### RT-002: Verify Sitemap and URL Structure
- **Decision**: Confirm that the target site's sitemap provides all necessary documentation pages
- **Rationale**: Need to ensure we can access all content that should be indexed
- **Alternatives considered**: Alternative crawling strategies if sitemap is incomplete

#### RT-003: Cohere Embedding Model Selection
- **Decision**: Which Cohere embedding model to use for documentation
- **Rationale**: Different models have different performance characteristics and costs
- **Alternatives considered**: Different Cohere embedding models (e.g., multilingual vs. English-optimized)

#### RT-004: Qdrant Collection Design
- **Decision**: How to structure Qdrant collection for optimal retrieval
- **Rationale**: Vector database design affects retrieval performance and metadata storage
- **Alternatives considered**: Different indexing strategies and metadata schemas

## Phase 1: Design & Contracts

### Data Model

#### DocumentChunk
- `id` (string): Unique identifier for the chunk (UUID)
- `url` (string): Source URL of the content
- `title` (string): Page title from the source
- `content` (string): Clean text content for embedding
- `content_length` (int): Length of content in characters
- `tokens` (int): Approximate token count
- `created_at` (datetime): When chunk was created
- `updated_at` (datetime): When chunk was last updated

#### EmbeddingVector
- `chunk_id` (string): Reference to DocumentChunk.id
- `vector` (list[float]): The embedding vector from Cohere
- `vector_size` (int): Dimension of the embedding vector
- `model_version` (string): Version of embedding model used

#### IndexingJob
- `id` (string): Unique identifier for the indexing job
- `status` (enum): ['pending', 'in_progress', 'completed', 'failed']
- `urls_to_process` (int): Total number of URLs to process
- `urls_processed` (int): Number of URLs processed
- `start_time` (datetime): When the job started
- `end_time` (datetime): When the job completed or failed
- `error_count` (int): Number of errors during processing

### API Contract

Since this is primarily a backend job rather than an API service, the main "contract" will be the function interfaces in the main.py file:

```
GET_ALL_URLS(sitemap_url) -> List[str]
  - Input: URL to sitemap XML
  - Output: List of URLs to crawl

EXTRACT_TEXT_FROM_URL(url) -> DocumentChunk
  - Input: URL to extract text from
  - Output: DocumentChunk object with content and metadata

CHUNK_TEXT(content, max_chunk_size, overlap) -> List[str]
  - Input: Content string, maximum chunk size, overlap size
  - Output: List of text chunks

EMBED(text_chunk) -> EmbeddingVector
  - Input: Text chunk to embed
  - Output: EmbeddingVector with vector data

CREATE_COLLECTION(collection_name, vector_size) -> boolean
  - Input: Name of collection and expected vector size
  - Output: Success boolean

SAVE_CHUNK_TO_QDRANT(chunk, embedding) -> boolean
  - Input: DocumentChunk and EmbeddingVector
  - Output: Success boolean

MAIN() -> Execution of full pipeline
  - Orchestrates the full process from URL extraction to storage
```

### Technology Stack

- **Language**: Python 3.9+
- **Package Management**: UV for fast dependency resolution
- **Web Scraping**: BeautifulSoup4 and requests
- **Embeddings**: Cohere Python client library
- **Vector Storage**: Qdrant Python client
- **Configuration**: python-dotenv for environment management

## Phase 1 Artifacts

### Project Structure
```
backend/
├── main.py
├── requirements.txt (or pyproject.toml if using poetry)
├── .env
├── .gitignore
└── README.md
```

### Quickstart Guide

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies with UV:
   ```
   uv venv
   uv pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   ```
5. Run the main script:
   ```
   python main.py
   ```

## Re-evaluation of Constitution Check Post-Design

The design aligns with all the constitution principles:
- Enables interdisciplinary collaboration through better access to documentation
- Respects ethical standards by only indexing public content
- Includes robust error handling and rate limiting
- Supports continuous learning by allowing updates to embeddings
- Uses standard technical approaches