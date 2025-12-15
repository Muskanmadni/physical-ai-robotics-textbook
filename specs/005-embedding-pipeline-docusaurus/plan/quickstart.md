# Quickstart Guide: Embedding Pipeline for Documentation Retrieval

## Prerequisites

- Python 3.9 or higher
- UV package manager installed
- Cohere API key
- Qdrant instance (local or cloud)
- Git (for repository cloning)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-book/backend
```

### 2. Install UV (if not already installed)
```bash
pip install uv
```

### 3. Create Virtual Environment and Install Dependencies
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the backend directory with the following content:
```
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here  
QDRANT_API_KEY=your_qdrant_api_key_here
TARGET_SITE_URL=https://physical-ai-robotics-textbook-three.vercel.app/
SITEMAP_URL=https://physical-ai-robotics-textbook-three.vercel.app/sitemap.xml
```

### 5. Run the Embedding Pipeline
```bash
python main.py
```

## Expected Output

When running the script, you should see progress logs indicating:
1. URLs being extracted from the sitemap
2. Text being extracted from each URL
3. Text being chunked into appropriate segments
4. Embeddings being generated for each chunk
5. Chunks being stored in Qdrant with metadata
6. Final completion status

## Troubleshooting

### Common Issues:

1. **API Rate Limits**: If you encounter rate limiting from Cohere:
   - Verify your API plan supports the volume of embeddings needed
   - Consider adding additional delays between requests

2. **Network Issues**: 
   - Ensure target URLs are accessible
   - Check for firewall restrictions if running in a restricted environment

3. **Qdrant Connection Issues**:
   - Verify Qdrant service is running and accessible
   - Check that the URL and API key in your .env file are correct

### Environment Setup Verification:
To verify your environment is set up correctly, you can run:
```bash
python -c "import cohere, qdrant_client, requests, bs4; print('All dependencies imported successfully')"
```