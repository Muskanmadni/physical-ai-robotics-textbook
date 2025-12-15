# Data Model: Embedding Pipeline for Documentation Retrieval

**Feature**: 005-embedding-pipeline-docusaurus
**Created**: 2025-12-15
**Status**: Complete

## DocumentChunk

Represents a segment of documentation content with associated metadata.

```python
class DocumentChunk:
    id: str              # Unique identifier (UUID)
    url: str             # Source URL of the content
    title: str           # Page title from the source
    content: str         # Clean text content for embedding
    content_length: int  # Length of content in characters
    tokens: int          # Approximate token count
    created_at: datetime # When chunk was created
    updated_at: datetime # When chunk was last updated
```

**Validation Rules:**
- `id` must be a valid UUID
- `url` must be a valid URL format
- `content` must not be empty
- `content_length` must be non-negative
- `tokens` must be non-negative
- `created_at` must be a valid datetime

## EmbeddingVector

Represents the numerical embedding of text content.

```python
class EmbeddingVector:
    chunk_id: str        # Reference to DocumentChunk.id
    vector: List[float]  # The embedding vector from Cohere
    vector_size: int     # Dimension of the embedding vector
    model_version: str   # Version of embedding model used
```

**Validation Rules:**
- `chunk_id` must match an existing DocumentChunk.id
- `vector` must be a list of floats
- `vector_size` must match the expected embedding dimension (1024 for Cohere v3)
- `model_version` must be non-empty

## IndexingJob

Represents a task for processing content from documentation sites.

```python
class IndexingJob:
    id: str              # Unique identifier for the indexing job
    status: str          # ['pending', 'in_progress', 'completed', 'failed']
    urls_to_process: int # Total number of URLs to process
    urls_processed: int  # Number of URLs processed
    start_time: datetime # When the job started
    end_time: datetime   # When the job completed or failed
    error_count: int     # Number of errors during processing
```

**Validation Rules:**
- `id` must be a valid UUID
- `status` must be one of the defined values
- `urls_to_process` must be non-negative
- `urls_processed` must be non-negative and not exceed urls_to_process
- `start_time` must be a valid datetime
- `error_count` must be non-negative

## State Transitions

### IndexingJob Status Transitions:
- `pending` → `in_progress`: When processing begins
- `in_progress` → `completed`: When all URLs are successfully processed
- `in_progress` → `failed`: When errors occur that prevent completion