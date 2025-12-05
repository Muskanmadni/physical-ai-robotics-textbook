from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance

# Initialize the sentence transformer model for embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

class RAGService:
    def __init__(self):
        # Initialize Qdrant client
        # In a real implementation, these values would come from environment variables
        self.client = QdrantClient(url="http://localhost:6333")  # or from env vars
        
        # Check if collection exists, if not create it
        try:
            self.client.get_collection("textbook_content")
        except:
            # Create collection for storing textbook content vectors
            self.client.create_collection(
                collection_name="textbook_content",
                vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(), distance=Distance.COSINE)
            )
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for a given text
        """
        embedding = model.encode(text)
        return embedding.tolist()
    
    def add_content(self, content_id: str, text: str, metadata: Dict[str, Any]):
        """
        Add content to the vector database
        """
        embedding = self.embed_text(text)
        
        # Add to Qdrant
        self.client.upsert(
            collection_name="textbook_content",
            points=[
                PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload={
                        "text": text,
                        "metadata": metadata
                    }
                )
            ]
        )
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for relevant content based on the query
        """
        query_embedding = self.embed_text(query)
        
        # Search in Qdrant
        search_results = self.client.search(
            collection_name="textbook_content",
            query_vector=query_embedding,
            limit=limit
        )
        
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "text": result.payload["text"],
                "metadata": result.payload["metadata"],
                "relevance_score": result.score
            })
        
        return results
    
    def query(self, query: str, user_id: str = None) -> Dict[str, Any]:
        """
        Main RAG query function - retrieves relevant content and generates response
        """
        # Search for relevant content
        search_results = self.search(query, limit=5)
        
        if not search_results:
            return {
                "response": "I couldn't find any relevant information to answer your query. The textbook may not contain information on this specific topic.",
                "sources": []
            }
        
        # In a real implementation, you would send the query + retrieved documents to an LLM
        # For now, we'll create a mock response
        response_text = f"Based on the textbook content: {'; '.join([result['text'][:100] for result in search_results[:2]])}..."
        
        sources = [
            {
                "chapterId": result["metadata"].get("chapter_id", "unknown"),
                "title": result["metadata"].get("title", "Unknown"),
                "relevance": result["relevance_score"]
            }
            for result in search_results
        ]
        
        return {
            "response": response_text,
            "sources": sources
        }

# Create a global instance of the service
rag_service = RAGService()