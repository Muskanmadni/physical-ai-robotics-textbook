from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging
from ..models.rag_models import RAGQueryRequest, RAGQueryResponse
from ..services.rag_service import RAGService

router = APIRouter()
logger = logging.getLogger(__name__)

# Global RAG service instance
rag_service = RAGService()


@router.post("/rag/query", response_model=RAGQueryResponse)
async def query_rag(request: RAGQueryRequest):
    """
    Query the RAG system for textbook-related information
    """
    try:
        logger.info(f"Processing RAG query: {request.query[:50]}...")
        response = await rag_service.query_rag(request)
        logger.info("RAG query processed successfully")
        return response
    except Exception as e:
        logger.error(f"Error processing RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.post("/rag/index")
async def index_content(chapter_id: str, title: str, content: str):
    """
    Index textbook content into the RAG system
    """
    try:
        logger.info(f"Indexing content for chapter: {chapter_id}")
        await rag_service.index_textbook_content(chapter_id, title, content)
        logger.info(f"Content for chapter {chapter_id} indexed successfully")
        return {"message": f"Content for chapter {chapter_id} indexed successfully"}
    except Exception as e:
        logger.error(f"Error indexing content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error indexing content: {str(e)}")