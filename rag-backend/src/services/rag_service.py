import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from cohere import Client as CohereClient
import google.generativeai as genai
from ..models.rag_models import RAGDocument, RAGQueryRequest, RAGQueryResponse, RAGSource
from ..utils.text_processor import TextProcessor
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Initialize Qdrant client with credentials from environment variables
        qdrant_url = os.getenv("QDRANT_URL", "https://ac35b1d0-4133-4e8e-a0f1-c88002cfdfc2.us-east4-0.gcp.cloud.qdrant.io:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")

        self.qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

        # Initialize Cohere client for embeddings
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.cohere_client = CohereClient(api_key=cohere_api_key)
        self.embed_model = "embed-english-v3.0"

        # Initialize Gemini client for response generation
        gemini_api_key = os.getenv("GOOGLE_API_KEY")
        if not gemini_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')

        # Collection name for storing textbook content
        self.collection_name = "textbook_content"

        # Initialize the collection if it doesn't exist
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize the Qdrant collection for storing textbook content."""
        try:
            # Check if collection exists
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} already exists")

            # Check if the vector size matches what we expect
            # If it doesn't match, we need to recreate the collection
            # The first vector config is what we're interested in
            vector_config = collection_info.config.params.vectors
            if hasattr(vector_config, 'size') and vector_config.size != 1024:
                logger.info(f"Vector size mismatch (expected 1024, got {vector_config.size}), recreating collection")
                self.qdrant_client.delete_collection(self.collection_name)
                self._create_collection()
            else:
                logger.info(f"Collection {self.collection_name} has correct vector size")
        except:
            # Collection doesn't exist, create it
            self._create_collection()

    def _create_collection(self):
        """Create the Qdrant collection with the correct configuration."""
        self.qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
        )
        logger.info(f"Created collection {self.collection_name}")
    
    async def index_textbook_content(self, chapter_id: str, title: str, content: str):
        """Index textbook content into the vector database."""
        # Split content into chunks
        text_processor = TextProcessor()
        chunks = text_processor.split_text(content)

        points = []
        for i, chunk in enumerate(chunks):
            # Create embedding for the chunk
            embedding = await self._create_embedding(chunk)

            # Qdrant expects point IDs to be either unsigned integers or UUIDs
            # Using a combination of chapter_id hash and chunk index as integer ID
            import hashlib
            # Create a unique integer ID based on chapter_id and chunk index
            hash_input = f"{chapter_id}_{i}".encode('utf-8')
            point_id = int(hashlib.md5(hash_input).hexdigest()[:8], 16) % (2**31)  # Convert to positive 32-bit integer

            point = models.PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "chapter_id": chapter_id,
                    "title": title,
                    "content": chunk,
                    "chunk_index": i
                }
            )
            points.append(point)

        # Upload points to Qdrant
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        logger.info(f"Indexed {len(points)} chunks for chapter {chapter_id}")
    
    async def query_rag(self, request: RAGQueryRequest) -> RAGQueryResponse:
        """Process a RAG query and return a response."""
        # Create embedding for the query
        query_embedding = await self._create_embedding(request.query)
        
        # Search in Qdrant using query_points (note: parameter name changed to 'query' in newer versions)
        search_results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=5,  # Return top 5 most relevant chunks
            with_payload=True
        ).points
        
        # Extract relevant content and sources
        context_parts = []
        sources = []
        
        for result in search_results:
            if result.payload:
                context_parts.append(result.payload["content"])
                sources.append(RAGSource(
                    chapterId=result.payload["chapter_id"],
                    title=result.payload["title"],
                    relevance=result.score
                ))
        
        # Combine context for the LLM
        context = "\n".join(context_parts)
        
        # Generate response using OpenAI
        response = await self._generate_response(request.query, context)
        
        return RAGQueryResponse(response=response, sources=sources)
    
    async def _create_embedding(self, text: str) -> List[float]:
        """Create an embedding for the given text using Cohere."""
        response = self.cohere_client.embed(
            texts=[text],
            model=self.embed_model,
            input_type="search_document"
        )
        return response.embeddings[0]
    
    async def _generate_response(self, query: str, context: str) -> str:
        """Generate a response using Gemini based on the query and context."""
        prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
        Use the following context to answer the user's question.
        If the context doesn't contain enough information, say so.

        Context: {context}

        Question: {query}

        Answer:
        """

        response = self.gemini_model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 500,
                "temperature": 0.3,
            }
        )

        return response.text