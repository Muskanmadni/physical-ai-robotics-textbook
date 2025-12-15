# Research Document: Embedding Pipeline Implementation

**Feature**: 005-embedding-pipeline-docusaurus
**Created**: 2025-12-15
**Status**: Complete

## Decision: Optimal Text Chunking Strategy

**Rationale**: Cohere's embedding models have token limits (typically 512 tokens for most models) that affect how we need to chunk text. For documentation retrieval, we need to balance semantic coherence with token efficiency. Documentation often has natural semantic boundaries (headers, sections) that make it ideal for context-aware chunking.

We'll use a strategy of:
- Maximum chunk size: 450 tokens (leaving buffer for API overhead)
- Overlap: 50 tokens to maintain context across chunks
- Boundary respect: Try to chunk at semantic boundaries when possible (after headers, paragraphs)

**Alternatives considered**:
- Fixed character length chunks: Less context-aware but simpler to implement
- Sentence-based chunks: More semantically coherent but potentially variable length

## Decision: Sitemap and URL Structure Verification

**Rationale**: The target site https://physical-ai-robotics-textbook-three.vercel.app/ has a sitemap at https://physical-ai-robotics-textbook-three.vercel.app/sitemap.xml. This will provide us with all the page URLs needed for indexing. 

I've verified the structure contains URLs to documentation pages that would be relevant for RAG retrieval.

**Alternatives considered**:
- Full web crawling: More comprehensive but requires more complex logic to identify relevant content
- Manual URL list: More control but less scalable for updates to the site

## Decision: Cohere Embedding Model Selection

**Rationale**: For English documentation content, Cohere's `embed-multilingual-v3.0` model is recommended as it works well with technical documentation. It produces 1024-dimensional embeddings and handles nuanced text well.

**Alternatives considered**:
- `embed-english-v3.0`: Optimized specifically for English but multilingual model also works well
- Earlier v2 models: Less capable than v3 models

## Decision: Qdrant Collection Design

**Rationale**: For the RAG use case, we need to store both the embedding vectors and metadata for context retrieval. The collection structure will be:

- Points in the collection will represent individual text chunks
- Payload will include the source URL, content, title, and other metadata
- Vector size will match the embedding model (1024 dimensions for Cohere v3 models)
- We'll use cosine similarity for similarity search

**Alternatives considered**:
- Different similarity metrics (Euclidean, Dot Product): Cosine is standard for text embeddings
- Different vector sizes: Based on chosen embedding model

## Additional Implementation Research

### Error Handling Strategy
- Network request retries with exponential backoff
- Cohere API rate limit handling with proper delays
- Database connection recovery strategies
- Progress tracking to allow resumption after failures

### Performance Considerations
- Parallel processing for fetching and cleaning text
- Batch embeddings for efficiency with Cohere API
- Batch upserts to Qdrant for efficiency

### Data Cleaning Approach
- Remove navigation elements, headers, footers using CSS selectors
- Preserve important semantic elements like headings for context
- Handle code blocks appropriately (include or exclude based on relevance)