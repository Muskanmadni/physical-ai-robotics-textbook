import os
import requests
import cohere
import google.generativeai as genai
import logging
from bs4 import BeautifulSoup
from qdrant_client import QdrantClient
from qdrant_client.http import models
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Request
import time
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Embedding Pipeline API",
              description="API for extracting text from documentation sites, generating embeddings, and storing in Qdrant for RAG",
              version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class IndexingJobStatus(BaseModel):
    job_id: str
    status: str
    urls_to_process: int
    urls_processed: int
    error_count: int
    created_at: datetime
    updated_at: datetime

class IndexingRequest(BaseModel):
    sitemap_url: str
    collection_name: str = "rag_embeddings"

class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 5

class AIResponseRequest(BaseModel):
    query: str
    context: str = ""

class AIResponse(BaseModel):
    response: str
    model_used: str

class EmbeddingPipeline:
    def __init__(self):
        # Initialize Cohere client
        self.cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

        # Target site and sitemap
        self.target_site_url = os.getenv("TARGET_SITE_URL", "https://physical-ai-robotics-textbook-three.vercel.app/")
        self.sitemap_url = os.getenv("SITEMAP_URL", "https://physical-ai-robotics-textbook-three.vercel.app/sitemap.xml")

        # Embedding model
        self.embedding_model = "embed-multilingual-v3.0"
        self.vector_size = 1024  # For Cohere's multilingual v3 model

    def get_all_urls(self, sitemap_url: str) -> List[str]:
        """
        Extract all URLs from the sitemap
        """
        logger.info(f"Fetching sitemap from {sitemap_url}")
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Parse the sitemap XML
        root = ET.fromstring(response.content)

        # Namespace handling for sitemap XML
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        urls = []
        for url_element in root.findall('sitemap:url', namespace):
            loc_element = url_element.find('sitemap:loc', namespace)
            if loc_element is not None:
                urls.append(loc_element.text)

        logger.info(f"Found {len(urls)} URLs in sitemap")
        return urls

    def extract_text_from_url(self, url: str) -> Dict[str, Any]:
        """
        Extract clean text from a given URL
        """
        logger.info(f"Extracting text from {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Try to get main content from common content containers
            # This may need adjustment based on the specific site structure
            content_selectors = [
                'main',           # Main content area
                '.main-content',  # Common class for main content
                '.content',       # Generic content class
                'article',        # Article tag
                '.post-content',  # Post content area
                '.documentation'  # Documentation specific
            ]

            content = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    content = content_element.get_text(separator=' ', strip=True)
                    break

            # If no specific content area found, try to get all text
            if not content:
                content = soup.get_text(separator=' ', strip=True)

            # Also extract the page title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "No Title"

            return {
                "url": url,
                "title": title,
                "content": content,
                "content_length": len(content)
            }
        except Exception as e:
            logger.error(f"Error extracting text from {url}: {e}")
            return {
                "url": url,
                "title": "Error",
                "content": "",
                "content_length": 0
            }

    def chunk_text(self, text: str, max_chunk_size: int = 1200, overlap: int = 100) -> List[str]:
        """
        Chunk text into smaller pieces with overlap
        """
        if len(text) <= max_chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + max_chunk_size

            # Try to break at sentence boundary if possible
            if end < len(text):
                # Look for a sentence boundary near the end
                sentence_end = text.rfind('. ', start + max_chunk_size - 200, start + max_chunk_size)
                if sentence_end != -1 and sentence_end > start + 500:  # Ensure not too short
                    end = sentence_end + 2  # Include the period
                else:
                    # Look for paragraph boundary
                    para_end = text.rfind('\n\n', start + max_chunk_size - 200, start + max_chunk_size)
                    if para_end != -1:
                        end = para_end + 2
                    else:
                        # Just break at max_chunk_size
                        end = start + max_chunk_size

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # Move start with overlap
            start = end - overlap

            # If the remaining text is less than max_chunk_size, add it as the last chunk
            if len(text) - start <= max_chunk_size:
                final_chunk = text[start:].strip()
                if final_chunk:
                    chunks.append(final_chunk)
                break

        logger.info(f"Text chunked into {len(chunks)} chunks")
        return chunks

    def embed(self, text_chunk: str) -> List[float]:
        """
        Generate embedding for a text chunk
        """
        try:
            response = self.cohere_client.embed(
                texts=[text_chunk],
                model=self.embedding_model,
                input_type="search_document"
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []

    def create_collection(self, collection_name: str) -> bool:
        """
        Create Qdrant collection for storing embeddings
        """
        try:
            # Check if collection already exists
            collections = self.qdrant_client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if collection_name in collection_names:
                logger.info(f"Collection {collection_name} already exists")
                return True

            # Create new collection
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,  # This is set to 1024 for Cohere's embed-multilingual-v3.0
                    distance=models.Distance.COSINE
                )
            )

            logger.info(f"Created collection {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False

    def save_chunk_to_qdrant(self, chunk_data: Dict[str, Any], embedding: List[float], collection_name: str) -> bool:
        """
        Save a text chunk and its embedding to Qdrant
        """
        try:
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "url": chunk_data["url"],
                    "title": chunk_data["title"],
                    "content": chunk_data["content"],
                    "content_length": chunk_data["content_length"],
                    "created_at": datetime.utcnow().isoformat()
                }
            )

            self.qdrant_client.upsert(
                collection_name=collection_name,
                points=[point]
            )

            logger.info(f"Saved chunk to Qdrant: {chunk_data['url'][:50]}...")
            return True
        except Exception as e:
            logger.error(f"Error saving to Qdrant: {e}")
            return False

    def run_pipeline(self, sitemap_url: str = None, collection_name: str = "rag_embeddings"):
        """
        Main function to execute the full pipeline
        """
        logger.info("Starting embedding pipeline...")

        # Use provided sitemap_url or fall back to default
        sitemap_to_use = sitemap_url or self.sitemap_url

        # Create collection in Qdrant
        if not self.create_collection(collection_name):
            logger.error("Failed to create Qdrant collection, exiting")
            return

        # Get all URLs from sitemap
        urls = self.get_all_urls(sitemap_to_use)

        # Process each URL
        processed_count = 0
        failed_count = 0

        for url in urls:
            # Extract text from URL
            chunk_data = self.extract_text_from_url(url)

            if not chunk_data["content"]:
                logger.warning(f"No content extracted from {url}")
                failed_count += 1
                continue

            # Chunk the text
            text_chunks = self.chunk_text(chunk_data["content"])

            for i, chunk_text in enumerate(text_chunks):
                # Create a copy of chunk_data with the specific chunk content
                current_chunk_data = chunk_data.copy()
                current_chunk_data["content"] = chunk_text
                current_chunk_data["content_length"] = len(chunk_text)

                # Generate embedding
                embedding = self.embed(chunk_text)

                if not embedding:
                    logger.error(f"Failed to generate embedding for chunk {i} of {url}")
                    failed_count += 1
                    continue

                # Save to Qdrant
                success = self.save_chunk_to_qdrant(current_chunk_data, embedding, collection_name)

                if not success:
                    logger.error(f"Failed to save chunk {i} of {url} to Qdrant")
                    failed_count += 1
                else:
                    processed_count += 1

        logger.info(f"Pipeline completed. Processed: {processed_count}, Failed: {failed_count}")
        return {"processed": processed_count, "failed": failed_count}


# In-memory storage for job status (in production, use a database)
indexing_jobs: Dict[str, IndexingJobStatus] = {}

@app.get("/")
def read_root():
    return {"message": "Embedding Pipeline API", "status": "running"}


@app.get("/health")
def health_check():
    """
    Health check endpoint for the API
    """
    return {"status": "healthy", "message": "Embedding Pipeline API is running"}


@app.post("/index", response_model=Dict[str, str])
def start_indexing(request: IndexingRequest):
    """
    Start an indexing job to process documentation from a sitemap
    """
    try:
        job_id = str(uuid.uuid4())

        # Initialize job status
        indexing_jobs[job_id] = IndexingJobStatus(
            job_id=job_id,
            status="in_progress",
            urls_to_process=0,
            urls_processed=0,
            error_count=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Create pipeline instance and run
        pipeline = EmbeddingPipeline()

        # Get URLs first to update job status
        urls = pipeline.get_all_urls(request.sitemap_url)
        indexing_jobs[job_id].urls_to_process = len(urls)

        # Process the pipeline
        result = pipeline.run_pipeline(request.sitemap_url, request.collection_name)

        # Update job status
        indexing_jobs[job_id].status = "completed"
        indexing_jobs[job_id].urls_processed = result["processed"]
        indexing_jobs[job_id].error_count = result["failed"]
        indexing_jobs[job_id].updated_at = datetime.utcnow()

        return {"job_id": job_id, "status": "completed", "message": f"Indexing completed. Processed: {result['processed']}, Failed: {result['failed']}"}

    except Exception as e:
        logger.error(f"Indexing job failed: {e}")
        if job_id in indexing_jobs:
            indexing_jobs[job_id].status = "failed"
            indexing_jobs[job_id].updated_at = datetime.utcnow()
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")


@app.get("/status/{job_id}", response_model=IndexingJobStatus)
def get_job_status(job_id: str):
    """
    Get the status of an indexing job
    """
    if job_id not in indexing_jobs:
        raise HTTPException(status_code=404, detail="Job ID not found")

    return indexing_jobs[job_id]


@app.post("/query")
async def query_documents(request: Request):
    """
    Query endpoint that matches frontend expectations
    Expected input: {"query_text": "question", "top_k": 3}
    Returns: {"answer": "...", "sources": [...]}
    """
    try:
        # Parse the request to get query_text and top_k
        request_json = await request.json()
        query_text = request_json.get("query_text", "")
        top_k = request_json.get("top_k", 5)

        # Initialize Cohere and Qdrant clients
        cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
        qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

        # Generate embedding for the query text
        query_embedding = cohere_client.embed(
            texts=[query_text],
            model="embed-multilingual-v3.0",
            input_type="search_query"
        ).embeddings[0]

        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name="rag_embeddings",
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Format results for the frontend
        sources = []
        for result in search_results:
            sources.append({
                "text": result.payload.get("content", "")[:200] + "..." if len(result.payload.get("content", "")) > 200 else result.payload.get("content", ""),
                "source": result.payload.get("url", ""),
                "title": result.payload.get("title", ""),
                "similarity": result.score
            })

        # Generate AI response using context from search results
        context_texts = [result.payload.get("content", "") for result in search_results]
        context = "\n\n".join(context_texts[:3])  # Use top 3 results as context

        # Initialize the Gemini model for AI response
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Prepare the prompt with context if provided
        if context:
            prompt = f"Context: {context}\n\nQuestion: {query_text}"
        else:
            prompt = query_text

        # Generate response
        ai_response = model.generate_content(prompt)

        return {
            "answer": ai_response.text,
            "sources": sources
        }

    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")



@app.get("/collections")
def list_collections():
    """
    List all Qdrant collections
    """
    try:
        qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

        collections = qdrant_client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        return {"collections": collection_names}
    except Exception as e:
        logger.error(f"Failed to list collections: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list collections: {str(e)}")


@app.post("/create-collection/")
async def create_collection_endpoint(request: Request):
    """
    Create collection endpoint that matches frontend expectations
    Expected input: {"collection_name": "name"}
    """
    try:
        request_json = await request.json()
        collection_name = request_json.get("collection_name", "rag_embeddings")

        # Initialize Qdrant client
        qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

        # Check if collection already exists
        collections = qdrant_client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if collection_name in collection_names:
            logger.info(f"Collection {collection_name} already exists")
            return {"status": "exists", "message": f"Collection {collection_name} already exists"}

        # Create new collection
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Using same vector size as Cohere's embed-multilingual-v3.0 model
                distance=models.Distance.COSINE
            )
        )

        logger.info(f"Created collection {collection_name}")
        return {"status": "created", "message": f"Collection {collection_name} created successfully"}
    except Exception as e:
        logger.error(f"Create collection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Create collection failed: {str(e)}")


@app.post("/recreate-collection/")
async def recreate_collection_endpoint(request: Request):
    """
    Recreate collection endpoint to fix dimension mismatch
    Expected input: {"collection_name": "name"}
    """
    try:
        request_json = await request.json()
        collection_name = request_json.get("collection_name", "rag_embeddings")

        # Initialize Qdrant client
        qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

        # Delete the collection if it exists
        collections = qdrant_client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if collection_name in collection_names:
            qdrant_client.delete_collection(collection_name)
            logger.info(f"Deleted existing collection: {collection_name}")

        # Create new collection with correct dimensions (1024 for Cohere's embed-multilingual-v3.0)
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Using correct vector size for Cohere's embed-multilingual-v3.0 model
                distance=models.Distance.COSINE
            )
        )

        logger.info(f"Recreated collection {collection_name} with correct dimensions")
        return {"status": "recreated", "message": f"Collection {collection_name} recreated successfully with correct dimensions"}
    except Exception as e:
        logger.error(f"Recreate collection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Recreate collection failed: {str(e)}")


@app.post("/ai-response", response_model=AIResponse)
def generate_ai_response(request: AIResponseRequest):
    """
    Generate AI response using Gemini 2.5 Flash model based on a query and optional context
    """
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Prepare the prompt with context if provided
        if request.context:
            prompt = f"Context: {request.context}\n\nQuestion: {request.query}"
        else:
            prompt = request.query

        # Generate response
        response = model.generate_content(prompt)

        return AIResponse(
            response=response.text,
            model_used="gemini-2.5-flash"
        )
    except Exception as e:
        logger.error(f"AI response generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI response generation failed: {str(e)}")


def main():
    """
    Main execution function for CLI usage
    """
    pipeline = EmbeddingPipeline()
    pipeline.run_pipeline()


if __name__ == "__main__":
    # Run the FastAPI application with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)