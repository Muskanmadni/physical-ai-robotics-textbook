# RAG Backend API Connection Guide

This document provides instructions on connecting your frontend to the deployed RAG backend API.

## API Endpoints

Once deployed on Vercel, your API endpoints will be available at:

### Health Check
- **GET** `https://your-vercel-project-url.vercel.app/api/health`

### RAG Query
- **POST** `https://your-vercel-project-url.vercel.app/api/rag/query`

Request Body:
```json
{
  "query": "Your question about the textbook",
  "context_size": 3
}
```

Response:
```json
{
  "response": "Generated response based on textbook content",
  "sources": [
    {
      "chapterId": "chapter_id",
      "title": "Chapter Title",
      "relevance": 0.85
    }
  ]
}
```

### Content Indexing
- **POST** `https://your-vercel-project-url.vercel.app/api/rag/index`

Request Body:
```json
{
  "chapter_id": "unique_chapter_id",
  "title": "Chapter Title",
  "content": "Full chapter content to index"
}
```

Response:
```json
{
  "message": "Content for chapter X indexed successfully"
}
```

## Environment Variables Required

The backend requires the following environment variables to be set in Vercel:

- `QDRANT_URL` - URL for Qdrant vector database
- `QDRANT_API_KEY` - API key for Qdrant
- `COHERE_API_KEY` - API key for Cohere embeddings
- `GOOGLE_API_KEY` - API key for Google Gemini

## Frontend Implementation Example

Here's an example of how to connect from your frontend:

```javascript
// Example fetch request to query the RAG API
async function queryRAG(question) {
  const response = await fetch('https://your-vercel-project-url.vercel.app/api/rag/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: question,
      context_size: 3
    })
  });

  const data = await response.json();
  return data;
}

// Example usage
queryRAG("What is Physical AI?").then(result => {
  console.log(result.response);
  console.log(result.sources);
});
```

## Troubleshooting

- If API calls return 500 errors, check that all required environment variables are properly set in Vercel
- Ensure your frontend is making requests with proper CORS headers
- Verify that the vector database is properly configured and accessible

## Additional Notes

- The backend requires Python >=3.9 due to the google-generativeai dependency. This is handled automatically in the Vercel deployment.