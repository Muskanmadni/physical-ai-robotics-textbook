import sys
from pathlib import Path
import json
import os

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import the RAG service
from src.services.rag_service import RAGService
from src.models.rag_models import RAGQueryRequest

# RAG service will be initialized on first use
rag_service = None

# For Vercel Python Serverless Functions
def handler(event, context):
    try:
        # Get the HTTP method and path
        http_method = event['httpMethod']
        path = event['path']
        body = event.get('body')
        
        # Parse the query parameters
        query_params = event.get('queryStringParameters') or {}
        
        if http_method == 'GET' and path == '/api/health':
            # Health check endpoint
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET',
                    'Access-Control-Allow-Headers': '*',
                },
                'body': json.dumps({
                    'status': 'healthy',
                    'message': 'RAG API is running'
                })
            }
        
        elif http_method == 'POST' and path == '/api/rag/query':
            # Handle RAG query requests
            if body:
                # Initialize RAG service if not already done
                global rag_service
                if rag_service is None:
                    rag_service = RAGService()

                request_data = json.loads(body)

                # Create a RAGQueryRequest object
                query_request = RAGQueryRequest(query=request_data.get('query', ''),
                                             userId=request_data.get('userId'))

                # Perform the RAG query
                import asyncio
                response = asyncio.run(rag_service.query_rag(query_request))
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'POST',
                        'Access-Control-Allow-Headers': '*',
                    },
                    'body': json.dumps(response.dict())
                }
            
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST',
                    'Access-Control-Allow-Headers': '*',
                },
                'body': json.dumps({'error': 'Missing request body'})
            }
        
        elif http_method == 'POST' and path == '/api/rag/index':
            # Handle content indexing requests
            if body:
                # Initialize RAG service if not already done
                global rag_service
                if rag_service is None:
                    rag_service = RAGService()

                request_data = json.loads(body)

                chapter_id = request_data.get('chapter_id')
                title = request_data.get('title')
                content = request_data.get('content')

                if not all([chapter_id, title, content]):
                    return {
                        'statusCode': 400,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'POST',
                            'Access-Control-Allow-Headers': '*',
                        },
                        'body': json.dumps({'error': 'Missing required fields'})
                    }

                # Index the content
                import asyncio
                asyncio.run(rag_service.index_textbook_content(chapter_id, title, content))
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'POST',
                        'Access-Control-Allow-Headers': '*',
                    },
                    'body': json.dumps({'message': f'Content for chapter {chapter_id} indexed successfully'})
                }
            
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST',
                    'Access-Control-Allow-Headers': '*',
                },
                'body': json.dumps({'error': 'Missing request body'})
            }
        
        else:
            # 404 for other routes
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Headers': '*',
                },
                'body': json.dumps({'error': 'Not Found'})
            }
    
    except Exception as e:
        # Handle any errors
        import traceback
        print(traceback.format_exc())  # Print the full traceback for debugging
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': '*',
            },
            'body': json.dumps({'error': str(e)})
        }